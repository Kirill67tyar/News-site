
class MyMixin(object):
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

    def view_get_prop(self):
        return self.get_prop()

    def get_title_upper(self, title):
        if isinstance(title, str):
            return title.upper()

        return title.title.upper



# В utils мы прописываем свои собственные миксины, которые потом можно использовать в контроллерах

# Кастомные миксины имеют смысл, когда в get_context_data - много повторяющейся логики
# или вообще в контроллерах есть какая-то повторяющаяся логика
