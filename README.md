# IMDB API Clone With DRF

## Final Project Links (Arranged According To Usage)

1. Admin Access

    * Admin Section: http://127.0.0.1:8000/admin/

2. Accounts

    * Registration: http://127.0.0.1:8000/api/account/register/
    * Login: http://127.0.0.1:8000/api/account/login/
    * Logout: http://127.0.0.1:8000/api/account/logout/

3. Stream Platforms

    * Create Element & Access List: http://127.0.0.1:8000/api/watch/stream/
    * Access, Update & Destroy Individual Element: http://127.0.0.1:8000/api/watch/stream/<int:streamplatform_id>/

4. Watch List

    * Create & Access List: http://127.0.0.1:8000/api/watch/
    * Access, Update & Destroy Individual Element: http://127.0.0.1:8000/api/watch/<int:movie_id>/

5. Reviews

    * Create Review For Specific Movie: http://127.0.0.1:8000/api/watch/<int:movie_id>/reviews/create/
    * List Of All Reviews For Specific Movie: http://127.0.0.1:8000/api/watch/<int:movie_id>/reviews/
    * Access, Update & Destroy Individual Review: http://127.0.0.1:8000/api/watch/reviews/<int:review_id>/

6. User Review

    * Access All Reviews For Specific User: http://127.0.0.1:8000/api/watch/user-reviews/?username=example

## References

[Build REST APIs with Django REST Framework and Python Udemy Course](https://www.udemy.com/course/django-rest-framework/?utm_source=adwords&utm_medium=udemyads&utm_campaign=LongTail_la.EN_cc.ROW&utm_content=deal4584&utm_term=_._ag_77879424134_._ad_535397245863_._kw__._de_c_._dm__._pl__._ti_dsa-1007766171312_._li_9069819_._pd__._&matchtype=&gclid=CjwKCAiAleOeBhBdEiwAfgmXf3W4s10xVwffE28ydhBYCo7QItFAMk1Q4Y8O3aIyKo7Lafi9oYz8FRoCM7cQAvD_BwE)