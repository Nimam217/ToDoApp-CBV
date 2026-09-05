from rest_framework import serializers
from ...models import Task


class TaskModelSerializer(serializers.ModelSerializer):
    task_url = serializers.SerializerMethodField("get_task_url")
    desc = serializers.ReadOnlyField(source="get_description")

    class Meta:

        model = Task
        fields = [
            "id",
            "title",
            "user",
            "description",
            "desc",
            "done",
            "task_url",
        ]
        read_only_fields = ["user", "task_url"]

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)

        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("desc", None)
            rep.pop("task_url", None)

        else:
            rep.pop("description", None)

        return rep

    def create(self, validated_data):

        validated_data["user"] = self.context.get("request").user
        return super().create(validated_data)

    def get_task_url(self, obj):
        request = self.context.get("request")

        return request.build_absolute_uri(obj.id)
