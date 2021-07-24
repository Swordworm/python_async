import uvicorn
import webbrowser

host_address = '127.0.0.1'
port = 8000


def main() -> None:
    """Function that runs server and opens browser."""
    webbrowser.open(f'{host_address}:{port}')
    uvicorn.run(app='application:app', host=host_address, port=port, reload=True)


if __name__ == '__main__':
    main()
