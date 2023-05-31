from integracao_hotmart import app

import os
from dotenv import load_dotenv
load_dotenv()

is_dev = os.getenv("DEBUG")

debug=False

if is_dev:
    debug=True
    
# debug = True faz com que toda mudança do código atualize automaticamente
if __name__ == '__main__':
    app.run(debug=debug)
