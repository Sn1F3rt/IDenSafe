from datetime import UTC, datetime

from siwe import SiweMessage, generate_nonce
from flask import flash, jsonify, request, url_for, redirect, render_template
from flask_login import login_user, logout_user, current_user, login_required

from factory import w3
from utils.crud import (
    add_user,
    revoke_kyc,
    activate_user,
    check_username,
    update_kyc_info,
    update_username,
    get_user_by_address,
    get_allowed_attributes,
    set_allowed_attributes,
)
from utils.forms import KYCForm, UsernameForm, AllowedAttributesForm

from . import auth_bp


@auth_bp.route("/auth/nonce/<address>", methods=["GET"])
def _nonce(address: str):
    address = w3.to_checksum_address(address)
    user = get_user_by_address(address)

    if user:
        return jsonify({"nonce": user.nonce}), 200

    nonce = generate_nonce()

    add_user(address, nonce)

    return jsonify({"nonce": nonce}), 200


@auth_bp.route("/auth/message/<address>", methods=["GET", "POST"])
def _message(address: str):
    address = w3.to_checksum_address(address)
    user = get_user_by_address(address)

    if not user:
        return jsonify({"error": "No nonce found for this address."})

    data = request.get_json()
    domain = data.get("domain")
    statement = data.get("statement")
    origin = data.get("origin")
    version = data.get("version")
    chain_id = data.get("chain_id")
    nonce = data.get("nonce")

    message = SiweMessage(
        domain=domain,
        address=address,
        statement=statement,
        uri=origin,
        version=version,
        chain_id=chain_id,
        issued_at=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        nonce=nonce,
    )

    return jsonify({"message": message.prepare_message()}), 200


@auth_bp.route("/auth/verify/<address>", methods=["POST"])
def _verify(address: str):
    address = w3.to_checksum_address(address)
    user = get_user_by_address(address)

    if not user:
        return jsonify({"error": "No nonce found for this address."})

    data = request.get_json()
    message = data.get("message")
    signature = data.get("signature")

    message = SiweMessage.from_message(message)

    try:
        message.verify(signature=signature, nonce=user.nonce)

    except Exception as e:
        return jsonify({"status": "error", "message": e.__str__()}), 400

    if not user.active:
        user = activate_user(address)

    login_user(user)
    flash("You have been logged in.", "success")

    return jsonify({"username": user.username})


@auth_bp.route("/auth/username/", methods=["GET", "POST"])
@login_required
def _username():
    if current_user.username:
        return redirect(url_for("app._index"))

    username_form = UsernameForm()

    if username_form.validate_on_submit():
        if check_username(username_form.username.data):
            flash("Username already taken.", "warning")
            return redirect(url_for("auth._username"))

        update_username(current_user.address, username_form.username.data)

        flash("Username updated successfully.", "success")

        return redirect(url_for("app._index"))

    return render_template("auth/username.html", username_form=username_form)


@auth_bp.route("/auth/logout", methods=["GET"])
@login_required
def _logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for("meta._index"))


@auth_bp.route("/auth/settings", methods=["GET", "POST"])
@login_required
def _settings():
    username_form = UsernameForm()

    if username_form.validate_on_submit():
        if current_user.username == username_form.username.data:
            flash("Old and new username cannot be the same.", "warning")
            return redirect(url_for("auth._settings"))

        if check_username(username_form.username.data):
            flash("Username already taken.", "warning")
            return redirect(url_for("auth._settings"))

        update_username(current_user.address, username_form.username.data)
        flash("Username updated successfully.", "success")
        return redirect(url_for("auth._settings"))

    return render_template("auth/settings.html", username_form=username_form)


@auth_bp.route("/auth/kyc", methods=["GET", "POST"])
@login_required
def _kyc():
    kyc_form = KYCForm()

    if kyc_form.validate_on_submit():
        update_kyc_info(
            current_user.address,
            kyc_form.name.data,
            kyc_form.age.data,
            kyc_form.location.data,
            kyc_form.id_number.data,
            kyc_form.id_front.data.read() if kyc_form.id_front.data else None,
            kyc_form.id_back.data.read() if kyc_form.id_back.data else None,
        )

        flash("Your KYC has been submitted for verification.", "success")
        return redirect(url_for("auth._kyc"))

    if current_user.verified:
        allowed_data_form = AllowedAttributesForm()
        allowed_attributes = get_allowed_attributes(current_user.address)

        if not all(allowed_attributes):
            allowed_data_form.name.default = int(allowed_attributes[0])
            allowed_data_form.age.default = int(allowed_attributes[1])
            allowed_data_form.location.default = int(allowed_attributes[2])
            allowed_data_form.id_number.default = int(allowed_attributes[3])
            allowed_data_form.process()

        if allowed_data_form.validate_on_submit():
            name = bool(int(allowed_data_form.name.data))
            age = bool(int(allowed_data_form.age.data))
            location = bool(int(allowed_data_form.location.data))
            id_number = bool(int(allowed_data_form.id_number.data))

            set_allowed_attributes(
                current_user.address, name, age, location, id_number
            )

            flash("Allowed attributes updated successfully.", "success")
            return redirect(url_for("auth._kyc"))

        return render_template(
            "auth/kyc.html", kyc_form=kyc_form, allowed_data_form=allowed_data_form
        )

    return render_template("auth/kyc.html", kyc_form=kyc_form)


@auth_bp.route("/auth/kyc/revoke", methods=["GET"])
@login_required
def _kyc_revoke():
    revoke_kyc(current_user.address)

    flash("Your KYC has been revoked.", "warning")
    return redirect(url_for("auth._kyc"))
