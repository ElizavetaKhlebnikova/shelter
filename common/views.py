class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


# class RequestForGuardianshipMixin:
#     template_name = 'pets/CatGuardianship.html'
#     form_class = RequestForCatGuardianshipForm
#     success_url = reverse_lazy('pets:cat_guardianship')  # куда нужно перейти после сохранения данных
#     success_message = 'Поздравляем! Вы успешно зарегистрированы!'
#     title = 'моя помощь котам'