# API Choice

- Étudiant : BOBJOK (or Student)
- API choisie : Frankfurter
- URL base : https://api.frankfurter.app
- Documentation officielle / README : https://www.frankfurter.app/docs/
- Auth : None
- Endpoints testés :
  - `GET /latest`
  - `GET /latest?from=INVALID`
- Hypothèses de contrat (champs attendus, types, codes) :
  - `GET /latest`: Returns 200 OK. Content-Type is JSON. Expected fields: `amount` (float/int), `base` (string), `date` (string), `rates` (object).
  - `GET /latest?from=INVALID`: Returns 404 Not Found. JSON body contains an error message.
- Limites / rate limiting connu : No strict rate limit documented, but we should limit requests to avoid abuse.
- Risques (instabilité, downtime, CORS, etc.) : Downtime or connection timeouts are possible since it's a free public API.
