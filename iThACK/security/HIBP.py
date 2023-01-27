from urllib.request import urlopen, Request


def get_hash_suffixes(hash_prefix):
    request = Request(f"https://api.pwnedpasswords.com/range/{hash_prefix}")
    request.add_header("Add-Padding", "true")
    with urlopen(request) as breached_hashes:
        return [items.decode("utf-8").split(":")[0] for items in breached_hashes.read().split()]


def have_i_been_pwned(password_hash):
    flag = False
    prefix = password_hash[:5]
    suffix = password_hash[5:]
    breached_suffixes = get_hash_suffixes(prefix)
    for hash_suffix in breached_suffixes:
        if suffix == hash_suffix.lower():
            flag = True
            break
    return flag
