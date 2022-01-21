from django.views.generic import ListView, DetailView
from mainapp.models import Article, ArticleCategories


class MainListView(ListView):
    """Класс для вывода списка «Хабров» на главной """
    template_name = 'mainapp/index.html'
    paginate_by = 9
    model = Article

    def get_context_data(self, **kwargs):
        # вызов базовой реализации для получения контекста
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        # добавляем в набор запросов все категории
        context['categories_list'] = ArticleCategories.objects.all()
        return context


class ArticleDetailView(DetailView):
    """Класс для вывода страницы статьи и подборок «Хабров» """
    template_name = 'mainapp/article_page.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Статья'
        context['title'] = title
        print(context)
        return context


class CategoriesListView(ListView):
    """Класс для вывода списка категорий """
    template_name = 'mainapp/categories.html'
    paginate_by = 9
    model = Article

    def get_queryset(self):
        # Объявляем переменную и записываем ссылку на id категории
        # article_id = self.request.GET.get('filter', 'give-default-value')
        categories_id = self.kwargs['pk']
        order = self.request.GET.get(categories_id)
        new_context = Article.objects.filter(name=categories_id).\
            order_by(order)
        return new_context

    def get_context_data(self, **kwargs):
        # вызов базовой реализации для получения контекста
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        category = ArticleCategories.objects.get(category_id)
        context['title'] = f'Статьи по категории {category.name}'
        # добавляем в набор запросов все категории
        context['categories_list'] = ArticleCategories.objects.all()
        return context


class LkListView(ListView):
    """Класс для вывода страницы ЛК """
    template_name = 'mainapp/user_lk.html'

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Личный кабинет'
        context['title'] = title
        return context
