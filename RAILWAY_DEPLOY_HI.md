# Railway deployment

## Deploy

1. Push this project folder to a GitHub repository.
2. In Railway, create a project using **Deploy from GitHub repo** and select that repository. Railway will build it with the included `Dockerfile`.
3. In the Railway service's **Variables**, set:
   - `ADMIN_KEY` — a long, private admin key.
   - `USER_KEY` — a different long, private user key.
   - Optionally, `FF_REGION` (defaults to `ID`).
4. In **Settings → Networking**, generate a Railway domain. Open the domain at `/`; unauthenticated visitors are redirected to the dashboard login at `/login`.
5. Keep **Auto Deploy** enabled for the connected GitHub branch; new pushes will trigger deployments.

Never commit actual keys or account credentials to GitHub. If an access key is missing, that login role stays disabled while the login page remains available. If both keys are set, they must be different. Keys are never printed to application logs.

## Keep dashboard data between deploys

Railway's container filesystem is temporary. If account data should survive redeploys, add a Railway volume and mount it at:

```text
/app/data
```

The app stores its `accounts.json`, token cache, and device data in that directory.

## Local Docker check

Create a local `.env` from `.env.example`, replace both placeholder keys with different private values, then run:

```sh
docker build -t paid-lv-up .
docker run --rm --env-file .env -p 8080:8080 paid-lv-up
```

Open `http://localhost:8080/` to reach the login page.
