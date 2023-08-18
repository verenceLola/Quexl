class Errors:
    @staticmethod
    def cleanErrorData(data: dict) -> dict:
        """
        remove empty objects in the present in response data
        """

        for field, errors in data.items():
            if isinstance(errors, list):
                errors = list(filter(lambda value: value != {}, errors))
                data[field] = errors
        error = data.get("error", data)

        return (
            {"message": data.pop("message"), "errors": data}
            if len(data) > 2
            else {"message": data.pop("message"), "error": error}
        )
