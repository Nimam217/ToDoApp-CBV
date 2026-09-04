{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user.first_name }} This is Your Activation Email
{% endblock %}

{% block html %}
    <a href="http://127.0.0.1:80/accounts/activation/{{ token }}/">
            Activate your account
    </a>
{% endblock %}