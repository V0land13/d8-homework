from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category, Priority
from collections import Counter

# Отработка сигналов для счетчиков категорий
@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_counter(sender, instance, action, model, **kwargs):
    print('Делаю task_cats_counter, action = ', action)
    if action == "post_add" or "post_remove":
        categories_all = []
        for c in Category.objects.all():
            categories_all.append(c.slug)
            #print(categories_all) 
        cat_counter = Counter()
        for t in TodoItem.objects.all():
            for cat in t.category.all():
                #print(cat.slug)
                if cat.slug in categories_all:
                    categories_all.remove(cat.slug)
                cat_counter[cat.slug] += 1
        for slug, new_count in cat_counter.items():
            Category.objects.filter(slug=slug).update(todos_count=new_count)
        #print(categories_all, 'это в конце')
        for ca in categories_all:
            Category.objects.filter(slug=ca).update(todos_count=0)
    else:
        return

# Отработка сигналов для счетчиков приоритетов

@receiver(post_save, sender=TodoItem)
def task_prior_counter(sender, instance, **kwargs):
    print('Делаю task_prior_counter, instance = ', instance)
    prior_all = []
    for p in Priority.objects.all():
        prior_all.append(p.slug)
    pr_counter = Counter()
    for ti in TodoItem.objects.all():
        #print(ti.priority.slug, type(ti.priority))
        if ti.priority.slug in prior_all:
            prior_all.remove(ti.priority.slug)
        pr_counter[ti.priority.slug] += 1
    for slug, new_count in pr_counter.items():
        Priority.objects.filter(slug=slug).update(priority_count=new_count)
    for pa in prior_all:
        Priority.objects.filter(slug=pa).update(priority_count=0)


# Отработка сигнала уделения задачи

@receiver(post_delete, sender=TodoItem)
def task_del(sender, instance, **kwargs):
    #print('del work instance =', instance)
    # обновляем счетчики категорий при удалении задачи
    cat_counter = Counter()
    categories_all = []
    for c in Category.objects.all():
        categories_all.append(c.slug)
    for t in TodoItem.objects.all():
        for cat in t.category.all():
            if cat.slug in categories_all:
                categories_all.remove(cat.slug)
            cat_counter[cat.slug] += 1
    for slug, new_count in cat_counter.items():
        Category.objects.filter(slug=slug).update(todos_count=new_count)
    for ca in categories_all:
        Category.objects.filter(slug=ca).update(todos_count=0)
    # обновляем счетчики приоритетов при удалении задачи
    pr_counter = Counter()
    prior_all = []
    for p in Priority.objects.all():
        prior_all.append(p.slug)
    for ti in TodoItem.objects.all():
        if ti.priority.slug in prior_all:
           prior_all.remove(ti.priority.slug)
        pr_counter[ti.priority.slug] += 1
    for slug, new_count in pr_counter.items():
        Priority.objects.filter(slug=slug).update(priority_count=new_count)
    for pa in prior_all:
        Priority.objects.filter(slug=pa).update(priority_count=0)  


# ТО ЧТО БЫЛО У АФТОРА МОДУЛЯ
# @receiver(m2m_changed, sender=TodoItem.category.through)
# def task_cats_added(sender, instance, action, model, **kwargs):
#     if action != "post_add":
#         return
#     print('add work')
#     for cat in instance.category.all():
#         slug = cat.slug

#         new_count = 0
#         for task in TodoItem.objects.all():
#             new_count += task.category.filter(slug=slug).count()

#         Category.objects.filter(slug=slug).update(todos_count=new_count)


# @receiver(m2m_changed, sender=TodoItem.category.through)
# def task_cats_removed(sender, instance, action, model, **kwargs):
#     if action != "post_remove":
#         return
#     print('remove work')
#     cat_counter = Counter()
#     for t in TodoItem.objects.all():
#         for cat in t.category.all():
#             cat_counter[cat.slug] += 1
#     print(cat_counter)
#     for slug, new_count in cat_counter.items():
#         Category.objects.filter(slug=slug).update(todos_count=new_count)