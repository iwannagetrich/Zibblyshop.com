# Zibblyshop.com

The shop at https://zibblyshop.com is `index.html`. Styles and the planner catalog are in that file. Product images stay on `i.etsystatic.com`, and checkout stays on the existing Etsy listings.

## Why this file has to stay

The working shop was a direct Vercel upload, deployment `dpl_AfTFdhMBCZLKUCnRYG2TH28pmjcL`. A later Git deploy of the README-only commit `5961ea3` (`dpl_34g1G4hM7rQPMfHxvPs6AFeY7Emf` and `dpl_J6vr24ZgrPZkPqc58h3oUkA9gM3i`) replaced it, and https://zibblyshop.com returned Vercel's 404. The domain was pointed back at the upload. This file is that page, copied from the live response, so the next Git deployment serves the shop instead of an empty repo.

Do not merge a commit that removes `index.html`.

## Vercel

Project `zibblyshop` (`prj_aj2kVhExDE57yoNi3Zvu0MGczykO`) on team `nate-afcc`. Framework is Other (`framework` null). `installCommand` and `buildCommand` are null, so there is no npm install and no build. Vercel serves `index.html` from the repository root.

`vercel.json` records those settings. Its ignore command runs `python3 -m unittest tests/test_storefront.py -q`. Vercel skips a deployment when that command exits 0 and builds when it exits 1, so the command is inverted: a passing test exits 1 and a failing test exits 0. A push without the catalog does not replace the deployment that is already live.

That skip applies to a deployment of a commit that contains this `vercel.json`. It is not in effect for production until this branch is merged to `main`.

## Seasonal campaign

The homepage is the Black Friday / Cyber Monday campaign. The hero is the New Year Reset Bundle: Fitness Planner, Meal Planner, and 2027 Planner. Product cards link straight to each Etsy listing. The 12-planner bundle is not on the page. The Christmas planner listing is still in the catalog.

Two values in the `EDIT HERE` script at the top of `index.html` control the campaign:

- `BLACK_FRIDAY_PERCENT` — the store-wide Etsy discount shown in the banner. Default `30`. Change this one number to match the live sale. Listing prices on the page are not rewritten.
- `NEW_YEAR_RESET_BUNDLE_URL` — the bundle button uses this. It is `https://www.etsy.com/ca/listing/4602697564`. That string appears once.

Fitness, Meal, and 2027 link to their existing Etsy listings (`4599144707`, `4599081891`, `4599086021`). Every product card says that 25% of every sale goes to Make-A-Wish.

## Check

```
python3 -m unittest tests/test_storefront.py -v
```

The test checks the 12 planners and their prices, the direct Etsy listing links, the Black Friday banner, and the New Year Reset Bundle hero.
