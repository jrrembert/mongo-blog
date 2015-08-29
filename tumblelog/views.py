from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form

from tumblelog.models import Post, Comment


posts = Blueprint('posts', __name__, template_folder='templates')


class ListView(MethodView):
    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):

    form = model_form(Comment, exclude=['created_date'])

    def get_context(self, slug):
        """ Get the default context for GET and POST requests. """
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            'post': post,
            'form': form
        }

        return context

    def get(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        return render_template('posts/detail.html', post=post)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        # If comment is valid, append comment to post
        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))

        return render_template('posts/detail.html', **context)



# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))