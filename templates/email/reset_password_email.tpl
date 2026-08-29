{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user }} This is Your Reset Password Email

{% endblock %}

{% block html %}
    <a href="http://127.0.0.1:80/accounts/api/v1/reset_password/confirm/{{ token }}/">
        Activate your account
    </a>
{% endblock %}