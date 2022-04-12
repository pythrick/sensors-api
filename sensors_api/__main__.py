import uvicorn
from typer import Typer

from config import settings

app = Typer()


@app.command()
def runserver():
    uvicorn.run(
        "sensors_api.api:app",
        debug=settings.debug,
        reload=settings.debug,
        host=settings.host,
        port=settings.port,
    )


def main():
    app()


if __name__ == "__main__":
    main()
