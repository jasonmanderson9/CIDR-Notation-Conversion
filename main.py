def calculate_subnet(ip_address, subnet_mask):
    ip_binary = ''.join(format(int(octet), '08b') for octet in ip_address.split('.'))
    subnet_mask_binary = ''.join(format(int(octet), '08b') for octet in subnet_mask.split('.'))

    network_id_binary = ''.join(
        [str(int(ip_bit) & int(subnet_bit)) for ip_bit, subnet_bit in zip(ip_binary, subnet_mask_binary)])
    network_id_decimal = '.'.join([str(int(network_id_binary[i:i + 8], 2)) for i in range(0, 32, 8)])

    inverted_subnet_mask_binary = ''.join(['1' if bit == '0' else '0' for bit in subnet_mask_binary])
    broadcast_ip_binary = ''.join(
        [str(int(ip_bit) | int(subnet_bit)) for ip_bit, subnet_bit in zip(ip_binary, inverted_subnet_mask_binary)])
    broadcast_ip_decimal = '.'.join([str(int(broadcast_ip_binary[i:i + 8], 2)) for i in range(0, 32, 8)])

    first_host_ip_binary = network_id_binary[:-1] + '1'
    first_host_ip_decimal = '.'.join([str(int(first_host_ip_binary[i:i + 8], 2)) for i in range(0, 32, 8)])

    last_host_ip_binary = broadcast_ip_binary[:-1] + '0'
    last_host_ip_decimal = '.'.join([str(int(last_host_ip_binary[i:i + 8], 2)) for i in range(0, 32, 8)])

    next_network_id_binary = bin(int(broadcast_ip_binary, 2) + 1)[2:].zfill(32)
    next_network_id_decimal = '.'.join([str(int(next_network_id_binary[i:i + 8], 2)) for i in range(0, 32, 8)])

    num_ips = 2 ** (32 - subnet_mask_binary.count('1'))

    num_ips_usable = num_ips - 2

    return {
        'Subnet Mask': subnet_mask,
        'Network ID': network_id_decimal,
        'Next Network': next_network_id_decimal,
        'Broadcast IP': broadcast_ip_decimal,
        'First Host IP': first_host_ip_decimal,
        'Last Host IP': last_host_ip_decimal,
        'Number of IP addresses': num_ips,
        'Number of usable IP Addresses': num_ips_usable
    }


def calculate_subnet_auto(ip_address_cidr):
    ip_address, cidr = ip_address_cidr.split('/')

    # Calculate subnet mask dynamically
    subnet_mask_binary = '1' * int(cidr) + '0' * (32 - int(cidr))
    subnet_mask_decimal = '.'.join([str(int(subnet_mask_binary[i:i + 8], 2)) for i in range(0, 32, 8)])

    return calculate_subnet(ip_address, subnet_mask_decimal)


# Example usage
ip_address_cidr = input("Enter the IP in the following format: 0.0.0.0/0: \n")

result_auto = calculate_subnet_auto(ip_address_cidr)

# Display the results
for key, value in result_auto.items():
    print(f'{key}: {value}')
