from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView,DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.urls import reverse_lazy
from .models import Article

#articles/url.py/でマッチしたら実行されるのがビュー

#subクラスで継承したいsuperクラスのimport順も重要
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    #template_nameは表示させるwebページのテンプレートのファイル名.
    #template_nameはListViewクラスで使う変数だから，他の名前にするとかはできない．
    template_name = 'article_list.html'
    login_url = 'login'



class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'
    login_url = 'login'

class ArticleUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Article
    #fielsdにはarticleの更新したいfieldを渡す．指定したfieldsがwebページ常に表記される
    #今回は，タイトルと本文を更新対象とするので，title, bodyとしている．
    #modelにはArticleを使っていて，Articleはfieldsにtitle, author, body, dateを持っている．
    #つまり，fields = ('author','title','body') とすれば，authorも変更できる．
    # （authorを変更することは普通はないから，含めていない．）
    #'date'もfieldsとしてあるが，dateはnon-editable fieldsなので，含めることは不可
    fields = ('title','body',)
    template_name = 'article_edit.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin,  DeleteView):
    model = Article
    template_name = 'article_delete.html'
    #投稿を削除した後のページのurl_nameが'article_list'
    success_url = reverse_lazy('article_list')
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    template_name = 'article_new.html'
    fields = ('title','body',)
    #login_urlはログインしていない状態で，articles/new/にアクセスした場合にリダイレクトするurl_nameである．
    #ログインしていないのにarticles/new/にアクセスして，新規投稿ができるのはおかしいから．
    login_url = 'login'

    #新規で投稿する場合，ログインしているユーザ名がauthorとなるようにしている．
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)