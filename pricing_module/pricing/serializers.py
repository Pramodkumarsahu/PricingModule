from rest_framework import serializers

class PriceInputSerializer(serializers.Serializer):
    total_km = serializers.FloatField()
    total_minutes = serializers.IntegerField()
    waiting_minutes = serializers.IntegerField()

    def validate(self, data):
        if data['total_km'] < 0:
            raise serializers.ValidationError("Total kilometers cannot be negative.")
        if data['total_minutes'] < 0:
            raise serializers.ValidationError("Total minutes cannot be negative.")
        if data['waiting_minutes'] < 0:
            raise serializers.ValidationError("Waiting minutes cannot be negative.")
        return data
