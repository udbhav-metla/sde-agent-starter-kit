import argparse
import uvicorn
from dotenv import load_dotenv
from .config import Settings
from .api import create_app


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Start the local SDE Agent console')
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    settings = Settings()
    print(f'Open local console: http://127.0.0.1:{args.port}/#token={settings.token}', flush=True)
    print('Single-user local service. Keep the login link private.', flush=True)
    uvicorn.run(create_app(settings), host='127.0.0.1', port=args.port, access_log=False)


if __name__ == '__main__':
    main()
