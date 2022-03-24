from email_validate import validate, validate_or_fail
is_valid = validate(
        email_address='lydiejoyer@8emesens.fr',
        check_format=True,
        check_blacklist=True,
        check_dns=True,
        dns_timeout=10,
        check_smtp=True,
        smtp_debug=True)

print(is_valid)