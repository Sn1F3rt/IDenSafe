from flask import request, render_template

from factory import w3
from utils.crud import verify_info, get_user_by_address, check_enabled_attribute

from . import meta_bp


@meta_bp.route("/", methods=["GET"])
def _index():
    return render_template("meta/index.html")


@meta_bp.route("/verify", methods=["GET"])
def _verify():
    address = request.args.get("address")
    name = request.args.get("name")
    age = request.args.get("age")
    location = request.args.get("location")
    id_number = request.args.get("id_number")

    if not address or not w3.is_address(address):
        return {"status": "error", "message": "Invalid address"}

    user = get_user_by_address(address)
    if not user or not user.verified:
        return {"status": "error", "message": "User not registered/verified"}

    if not any([name, age, location, id_number]):
        return {"status": "error", "message": "No verification parameters provided"}

    if age:
        try:
            age = int(age)

        except ValueError:
            return {"status": "error", "message": "Invalid age"}

    if not all(
        [
            check_enabled_attribute(address, attr, value)
            for attr, value in [
                ("name", name),
                ("age", age),
                ("location", location),
                ("id_number", id_number),
            ]
        ]
    ):
        return {
            "status": "error",
            "message": "One or more attribute(s) not allowed by user",
        }

    res = verify_info(address, name, age, location, id_number)

    return {"status": "success", "result": res}
