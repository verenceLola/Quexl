"""serializers for orders models"""
import asyncio
import os

import requests
from requests.auth import HTTPBasicAuth
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from quexl.apps.orders.models import DataFile
from quexl.apps.orders.models import History
from quexl.apps.orders.models import Order
from quexl.apps.orders.models import Parameter


class ParameterSerializer(serializers.ModelSerializer):
    """
    serializer for the parameter model
    """

    class Meta:
        model = Parameter
        fields = "__all__"


async def check_status(queryset):  # pragma: no cover
    api_key = os.environ["EXTERNAL_API_KEY"]
    try:
        uri = "https://sandbox.zamzar.com/v1/jobs/{}".format(queryset.job_id)
        response = requests.get(uri, auth=HTTPBasicAuth(api_key, ""))
        return response
    except BaseException:
        raise NotFound("Resource not found")


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the order model"""

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = (
            "buyer",
            "job_id",
            "history",
            "created_at",
            "updated_at",
        )

    output_url = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    currency_type = serializers.SerializerMethodField()

    def get_output_url(self, resp):  # pragma: no cover
        async def main():
            response = await check_status(resp)
            return response

        res = asyncio.run(main())
        if res.json()["status"] == "successful":
            file_id = res.json()["target_files"][0]["id"]
            endpoint = "https://sandbox.zamzar.com/v1/files/{}/content".format(
                file_id
            )
        else:
            endpoint = "Still {}...".format(res.json()["status"])
        return endpoint

    def get_total_price(self, obj):
        """Returns the total charge of the service"""
        service_price = obj.service.price
        parameter_temp_price = (
            obj.parameter.parameter_template.parameter_option.price
        )
        total = float(parameter_temp_price.amount) + float(
            service_price.amount
        )
        return total

    def get_currency_type(self, obj):
        """Returns the currence used"""
        currency = obj.service.price.currency
        return currency.code

    def create(self, validated_data):  # pragma: no cover  #TODO
        """create an order with the buyer as the logged in user"""
        validated_data.update({"buyer": self.context["request"].user})

        async def request_order():
            api_key = os.environ["EXTERNAL_API_KEY"]
            endpoint = validated_data["service"].api_endpoint
            source_file = validated_data["data_file"].data_file_upload
            target_format = validated_data[
                "parameter"
            ].parameter_template.data_format.name
            file_content = {"source_file": source_file}
            data_content = {"target_format": target_format}
            res = requests.post(
                endpoint,
                data=data_content,
                files=file_content,
                auth=HTTPBasicAuth(api_key, ""),
            )
            try:
                validated_data.update({"job_id": res.json()["id"]})
                uri = "https://sandbox.zamzar.com/v1/jobs/{}".format(
                    res.json()["id"]
                )
                if res.status_code == 201:
                    data = {}
                    data["output_url"] = uri
                    data["data_file"] = [validated_data["data_file"].id]
                    data["history_owner"] = validated_data["buyer"].id
                    serializer = HistorySerializer(data=data)
                    if serializer.is_valid(raise_exception=True):
                        hist = serializer.save()
                    validated_data.update({"history": hist})
                return res.json()["status"]
            except BaseException:
                raise NotFound(res.json())

        async def main():
            await request_order()
            order = Order.objects.create(**validated_data)
            return order

        order = asyncio.run(main())
        return order


class DataFileSerializer(serializers.ModelSerializer):
    """serializer class for DataFile model"""

    class Meta:
        model = DataFile
        fields = "__all__"

    def create(self, validated_data):
        validated_data.update({"file_owner": self.context["request"].user})
        data_file = DataFile.objects.create(**validated_data)
        return data_file


class HistorySerializer(serializers.ModelSerializer):
    """Serializer for the history model"""

    class Meta:
        model = History
        fields = "__all__"
