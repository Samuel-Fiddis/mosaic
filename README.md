# Mosaic App

A single page webapp for image adjustment and the creation of mosaic images.

![Advanced Search Example](images/example.png)

## Run Locally

To run locally simply run the docker compose file with:

```bash
  docker compose up --build
```

and connect to `localhost:3000` in your local browser :)

To improve the mosaic creation algorithm just increate the NUM_POINTS env var in the `docker-compose.yaml` file.