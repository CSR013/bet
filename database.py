usuarios_pagos = set()

def liberar_usuario(user_id):
    usuarios_pagos.add(str(user_id))

def verificar_usuario(user_id):
    return str(user_id) in usuarios_pagos