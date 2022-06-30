from configs import get_configs

token_service_data = {
    'algorithm': get_configs().algorithm,
    'exp_time': get_configs().exp_time,
    'secret_key': get_configs().secret_key
}
