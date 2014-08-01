from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost

wp = Client('http://whatsfreshstl.com/xmlrpc.php', 'tony', '!9oftides*5')

def newPost(title, content, tags, cats):
    post = WordPressPost()
    post.title = title
    post.content = content
    post.post_status = 'publish'
    post.terms_names = {
    'post_tag': tags,
    'category': cats 
    }
    wp.call(NewPost(post))
 