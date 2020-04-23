from django_serializable_model import SerializableModel

class FkSerializableModel(SerializableModel):
    class Meta:
        abstract = True

    def serialize(self, *args, **kwargs):
        joins = list()
        for field in self._meta.fields:
            if field.get_internal_type() == "ForeignKey":
                joins.append(field.name)
        args = joins + list(args)
        return super().serialize(*args, **kwargs)

