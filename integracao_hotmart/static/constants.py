ALL_ACTIONS = {
    "access_release":{
        "name": "access_release",
        "message": "Liberar acesso do e-mail: {email}",
        "description": "Acesso ao curso foi liberado.",
        "message_error": "Falha ao liberar acesso do e-mail: {email}",
        "description_error": "Servidor caiu, acesso ao curso não foi liberado."
    },
    "send_email_welcome":
        {
        "name": "send_email_welcome",
        "message":  "Enviar mensagem de boas vindas para o email: {email}",
        "description": "E-mail de boas vindas enviado.",
        "message_error":  "Falha ao enviar mensagem de boas vindas para o email: {email}",
        "description_error": "Serviço de e-mails fora do ar, e-mail de boas vindas não foi enviado."
    },
    "send_email_payment_declined":
        {
        "name": "send_email_payment_declined",
        "message":  "Enviar mensagem de pagamento recusado para o email: {email}",
        "description": "E-mail de pagamento recusado enviado.",
        "message_error":  "Falha ao enviar mensagem de pagamento recusado para o email: {email}",
        "description_error": "Serviço de e-mails fora do ar, e-mail de pagamento recusado não foi enviado."
    },
    "access_revoke":
        {
        "name": "access_revoke",
        "message":  "Remover acesso do e-mail: {email}",
        "description": "Acesso ao curso foi revogado.",
        "message_error":  "Falha ao remover acesso do e-mail: {email}",
        "description_error": "Servidor caiu, acesso ao curso não foi revogado."
    },
    "unmapped_status":
        {
        "name": "unmapped_status",
        "message":  "Status não reconhecido: {email}",
        "description": "Status não mapeado, consulte o desenvolvedor.",
        "message_error":  "Falha ao executar ação de status não reconhecido do e-mail: {email}",
        "description_error": "Falha ao tratar status não mapeado, consulte o desenvolvedor."
    }
          
}