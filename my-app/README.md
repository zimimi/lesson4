## Jooble_lesson2
This is the Lesson2

Реалізація через AWS http://3.64.55.199/read_posts

Реалізація API з CRUD на основі фреймворку Flask, який дозволяє створювати Веб-сайти на основі мови Python.

Для реалізації проекту використовується база даних SQLite та бібліотека SQLAlchemy, яка допомагає зв'язати обрану базу даних із Flask проектом.


## Resources and Actions

    URL                           HTTP         Operation
    /read_posts                   GET          Get a collection of posts.
    /read_posts?id=$value         GET          Show post by id. Example: /read_posts?id=2
    /read_posts?lim=$value        GET          Show last n posts. Example: /read_posts?lim=3
    /create_post                  GET          Create post.
    /read_posts/$id/delete        GET          Delete post number $id
    /read_posts/$id/update_post   GET          Update post number $id
