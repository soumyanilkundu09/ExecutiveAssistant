# Looksy AI vs. AI Vastra — Hardware Requirements & Integration Effort for a Tablet Kiosk Deployment

## Preliminary flag: product identity is unclear

### Takeaway
Across all searches, "Looksy AI" and "AI Vastra" resolve to **web-based / Shopify-app virtual try-on widgets for online stores**, not to standalone in-store tablet-kiosk hardware products. No official documentation, case study, or press material was found showing either product running as a dedicated in-store kiosk app (the kind implied by the "tablet-based virtual try-on" line in Ma Lakhsmi Stores' planned tool stack). This is a material gap that should be resolved (e.g., by contacting the vendors directly) before committing budget to tablets sized around these two names specifically.

### Cited Findings
- "Looksy AI Virtual Try-On" is a Shopify App Store listing (developer based in San Francisco per the listing, though the company's own site suggests Dubai) that adds a try-on button to **online product pages**; shoppers upload a photo to preview an item — [Looksy AI Virtual Try-On – Shopify App Store](https://apps.shopify.com/looksyai)
- Looksy's own marketing site describes it as an "AI virtual try-on and AI shopping assistant for online stores," explicitly aimed at e-commerce brands, not physical retail — [About Looksy](https://looksy.tech/about_us)
- Looksy's widget "runs inside the store's own interface" and is described as "fully responsive and works on all devices and screen sizes" — this is a responsive web statement about a storefront widget, not a spec for a standalone kiosk tablet app — [About Looksy](https://looksy.tech/about_us)
- "Ai Vastra: Virtual Try-On" is a Shopify App Store listing by developer "Nice Interactive" (based in Rajahmundry, Andhra Pradesh, India), covering men's/women's/kids' wear including Indian garments (sarees, kurtas, lehengas) and Western wear; it operates through **Shopify Admin** on product listings — [Ai Vastra: Virtual Try-On – Shopify App Store](https://apps.shopify.com/aivastra)
- AI Vastra launched on Shopify's app store on 24 August 2026 and had no reviews/ratings at time of research — [Ai Vastra: Virtual Try-On – Shopify App Store](https://apps.shopify.com/aivastra)
- A Google Play listing titled "Vastra: AI Digital Wardrobe" (developer "A2Kay") exists, but this is a personal digital-wardrobe/outfit-planning app, not a retail try-on kiosk tool, and is a different product from the Shopify "AI Vastra" — [Vastra: AI Digital Wardrobe – Google Play](https://play.google.com/store/apps/developer?id=A2Kay)
- A separate "Outfit Planner - Looksy" app exists on the Apple App Store, described as "Designed for iPad," but this is a personal closet/outfit-organizer consumer app, unrelated to the Shopify Looksy AI try-on widget — [Outfit Planner - Looksy – App Store](https://apps.apple.com/us/app/-/id6754006200)

### Inferences
- The names "Looksy AI" and "AI Vastra" in Ma Lakhsmi Stores' planned tool stack most likely refer to these Shopify try-on apps (or similarly-branded web widgets), which were designed for **e-commerce product pages**, not purpose-built in-store tablet kiosks. Running either on an in-store tablet would likely mean opening the store's Shopify-powered website in a tablet browser/kiosk-mode browser and using the same try-on widget customers get online — not a dedicated native kiosk app with its own hardware integration.
- Because neither product is a native kiosk product, there is no vendor-specified kiosk hardware stack (depth sensors, specific camera rigs, body scanners) tied to either brand name — any hardware decisions would default to generic tablet/webcam specs, not vendor requirements.

### Gaps
- No vendor contact, sales page, or spec sheet was found for either product in a dedicated "in-store/tablet kiosk" configuration. This should be confirmed directly with each vendor (Looksy: looksy.tech; AI Vastra/Nice Interactive: via the Shopify app listing) before assuming compatibility with the Premium Lounge plan.
- It's possible Soumyanil's original source used these names loosely for a *category* of AI try-on tool rather than a specific verified vendor; worth revisiting `context/work.md` wording after vendor confirmation.

---

## What tablet/device specs (OS, camera, processing power, screen size) does each product require or recommend?

### Takeaway
Neither Looksy nor AI Vastra publishes tablet-specific hardware specs; both are described only as responsive web/Shopify-admin tools with no stated OS, camera, or processor requirements.

### Cited Findings
- Looksy's site states the try-on widget is "fully responsive and works on all devices and screen sizes," with no camera, OS, browser, or processor specification given — [About Looksy](https://looksy.tech/about_us)
- The Looksy Shopify listing confirms the tool is used via photo upload (shopper uploads a photo; no live camera capture requirement is mentioned) — [Looksy AI Virtual Try-On – Shopify App Store](https://apps.shopify.com/looksyai)
- AI Vastra's Shopify listing likewise describes photo-based try-on ("see how outfits naturally look and drape") with no device/camera/OS specification published on the listing — [Ai Vastra: Virtual Try-On – Shopify App Store](https://apps.shopify.com/aivastra)
- For comparison, general industry-grade in-store virtual-try-on kiosks (not Looksy/AI Vastra specifically) are described by vendors as needing "spacious touchscreen kiosks" with "adjusted lighting, high-speed processors, and sensors," sometimes with added ring-lighting/calibrated LEDs for realistic previews — [Glamar — Virtual try-on mirror](https://www.glamar.io/solutions/vto/virtual-try-on-mirror)

### Inferences
- Since both tools appear to be browser-based/photo-upload widgets, the realistic minimum spec for a tablet running either is: a mid-range Android or iPad tablet (8–11"), a modern mobile browser (Chrome/Safari), a front or rear camera adequate for a decent selfie/outfit photo, stable Wi-Fi, and enough RAM/CPU to run a modern browser smoothly — not a special-purpose device. This is an inference, not a vendor spec.
- No evidence either tool needs high processing power on-device — both appear to do the AI image generation server-side (cloud), meaning the tablet is mainly a browser/display terminal with enough connectivity and screen quality for a convincing in-store presentation.

### Gaps
- No confirmed minimum screen size, RAM, OS version, or camera resolution from either vendor.
- No confirmed statement on whether the AI processing happens cloud-side (most likely, given the credit-based billing model described below) or on-device.

---

## Does either product require special hardware beyond a standard tablet (e.g. depth sensors, specific camera rigs, body-scanning hardware)?

### Takeaway
No evidence that either Looksy or AI Vastra requires depth sensors, specialized camera rigs, or body-scanning hardware — both rely on a single uploaded 2D photo, unlike other Indian in-store try-on vendors that do use such hardware.

### Cited Findings
- Looksy's process is photo-upload-based ("shopper uploads a photo to preview an item," "20 seconds" turnaround for a result), implying standard 2D image input, not 3D/depth capture — [Looksy AI Virtual Try-On – Shopify App Store](https://apps.shopify.com/looksyai); [About Looksy](https://looksy.tech/about_us)
- AI Vastra's listing describes the same pattern: shoppers upload a selfie to get an AI-generated preview; no mention of depth sensors or scanning hardware — [Ai Vastra: Virtual Try-On – Shopify App Store](https://apps.shopify.com/aivastra)
- By contrast, other Indian retail-tech vendors in the same space *do* use special hardware: Trupik (Hyderabad) uses 3D cameras to scan customers and drape garments on a 3D digital replica; Van Heusen's Style Studio (Bengaluru) uses a floor-to-ceiling monitor with mirror-image body scanning; PointAI (showcased with Aditya Birla Fashion and Retail) does near-instant in-store virtual try-on — [Apparel Resources — AI turns visual merchandising into visual experience](https://apparelresources.com/technology-news/retail-tech/ai-turns-visual-merchandising-visual-experience-retail/); [NewsBytes — PointAI partners with ABFRL](https://www.newsbytesapp.com/news/business/pointai-partners-with-abfrl-to-showcase-in-store-virtual-try-ons/tldr)
- Tanishq's in-store virtual showroom (built by DaveAI) runs on tablets with an avatar-led 3D-rendered experience, showing that tablet-based deployments in Indian retail do exist as a category, but this is a jewelry showroom product, not a garment try-on tool, and is unrelated to Looksy/AI Vastra — [iamdave.ai — Tanishq case study](https://www.iamdave.ai/stories/tanishq/)
- Academic literature on saree-specific virtual try-on (a 2025 paper in the Journal of Advances in Information Technology) describes an AR/smart-mirror system that requires customers to input body measurements and uses AR draping — a different technical approach from simple photo-upload tools, and not tied to either Looksy or AI Vastra — [JAIT V16N3 426 (PDF)](https://www.open-access.bcu.ac.uk/17060/1/JAIT-V16N3-426.pdf)

### Inferences
- If Looksy or AI Vastra are indeed the photo-upload Shopify-style tools found in this research, Ma Lakhsmi Stores would **not** need depth sensors or body-scanning rigs for them specifically — a standard tablet camera (or even manual photo upload from a staff phone) would suffice.
- However, the fit/drape realism of a simple 2D photo-upload try-on is likely lower than hardware-assisted systems (3D scan/AR drape) used by Trupik or the smart-mirror research system — a relevant trade-off for a "Premium Lounge" positioning aiming at a high-trend, status-conscious customer base.

### Gaps
- No direct vendor confirmation (from Looksy or AI Vastra) ruling in/out optional depth-sensor or AR add-ons for an enterprise/in-store tier — the public listings found only describe the e-commerce consumer flow.

---

## What is the typical setup/installation process and timeline (self-serve app install vs. vendor-assisted deployment)?

### Takeaway
Looksy explicitly advertises a fast, vendor-assisted, no-code setup ("most brands go live within one business day… IT team does no work"); AI Vastra's process is a standard Shopify app install with no stated timeline or vendor-assistance claim.

### Cited Findings
- Looksy: "Most brands go live within one business day. Looksy handles the full setup, and the store's IT team does no work. No developer is needed." — [About Looksy](https://looksy.tech/about_us)
- Looksy supports Shopify, WooCommerce, Magento, Bitrix, and custom-built websites as integration targets — [About Looksy](https://looksy.tech/about_us)
- AI Vastra: installed directly from the Shopify App Store; requires a Shopify account, store selection, and granting store data access (viewing store owner details, editing products/collections, viewing the Online Store theme) — [Ai Vastra: Virtual Try-On – Shopify App Store](https://apps.shopify.com/aivastra)
- AI Vastra's listing does not describe a setup timeline, vendor-assisted onboarding, or theme/storefront installation steps beyond the Shopify install flow — [Ai Vastra: Virtual Try-On – Shopify App Store](https://apps.shopify.com/aivastra)

### Inferences
- Both tools assume the retailer already runs (or is willing to run) a Shopify or similar e-commerce storefront — Ma Lakhsmi Stores would need an actual online store/website live before either tool's standard install path applies. This matters directly for the "functional website" Q4 2026 goal and the April 2027 launch window: the website needs to exist first, and these try-on tools would most naturally bolt onto it.
- For a tablet kiosk use case specifically (rather than online checkout), setup would likely mean: build/launch the Shopify (or similar) storefront → install the try-on app on it → open that storefront in kiosk/browser-lock mode on the two Premium Lounge tablets. This is a reasonable inferred path, not a documented one.

### Gaps
- Neither vendor publishes a specific "in-store tablet kiosk mode" setup guide or timeline; the one-day timeline cited for Looksy applies to e-commerce site installation, not kiosk hardware deployment.
- No information on kiosk-mode lockdown, staff training requirements, or hardware provisioning timelines from either vendor.

---

## Does either product integrate with retail POS/inventory systems like Marg ERP or Zoho Inventory, or does it operate as a standalone kiosk app unrelated to inventory?

### Takeaway
No evidence either product integrates with Marg ERP, Zoho Inventory, or any POS/inventory system; both operate purely against the store's e-commerce catalog (Shopify products/collections), with no mention of POS or inventory system connectivity anywhere in their public materials.

### Cited Findings
- AI Vastra's requested Shopify permissions are limited to "viewing store owner details, editing products and collections, and viewing the Online Store theme" — i.e., it reads/writes the Shopify product catalog only, with no mention of POS, billing, or external inventory system integration — [Ai Vastra: Virtual Try-On – Shopify App Store](https://apps.shopify.com/aivastra)
- Looksy's own materials describe a try-on widget, product recommendation engine, and sales-impact analytics dashboard, all scoped to the e-commerce storefront and its catalog — no POS/inventory integration is mentioned — [About Looksy](https://looksy.tech/about_us)
- Neither vendor's page mentions Marg ERP, Zoho Inventory, Tally, or any India-specific POS/inventory product by name (confirmed absence, not found in any search result).

### Inferences
- Both tools would operate as **standalone catalog-dependent apps**: they need product data (images, descriptions) from wherever the online catalog lives (presumably Shopify or similar), but they do not talk to a backend POS/inventory system like Marg ERP or Zoho Inventory. Stock levels, SKU tagging by fabric/trend/origin (per `current-priorities.md` priority #1) would need to be maintained separately in Marg ERP/Zoho Inventory and then mirrored manually (or via a separate Shopify-Marg/Zoho sync, if one exists) into whatever catalog powers the try-on tool.
- This means deploying either try-on tool does not reduce or replace the need to finish the POS/inventory rollout (current priority #1) — they are unrelated systems that would need to be kept in sync independently.

### Gaps
- No research was done (out of this task's scope) on whether Marg ERP or Zoho Inventory themselves offer a Shopify sync/connector — that would be the missing link for keeping a try-on tool's catalog current with real inventory, and is worth a separate research pass if this integration path is pursued.

---

## What ongoing technical maintenance does each require (software updates, internet connectivity requirements, offline capability)?

### Takeaway
Both tools appear to be cloud/SaaS-hosted services with credit-based billing, implying mandatory internet connectivity and no offline capability; software updates would be handled vendor-side (typical of SaaS apps), but neither vendor publishes explicit uptime, connectivity, or offline-mode statements.

### Cited Findings
- Looksy: "Usage is credit-based. Brands can top up anytime and receive a warning before the balance runs low" — confirming a cloud/metered-usage billing model, which requires an active internet connection to function (image generation happens server-side) — [About Looksy](https://looksy.tech/about_us)
- Looksy provides a real-time analytics dashboard (try-on counts, engagement, sales impact), another indicator of a connected, server-hosted service — [About Looksy](https://looksy.tech/about_us)
- AI Vastra's pricing is credit-based (one-time credit purchases: Free 25 credits/5 try-ons, Silver $10/160 try-ons, Gold $25/450 try-ons, Platinum $100/2,000 try-ons), again implying server-side processing requiring connectivity — [Ai Vastra: Virtual Try-On – Shopify App Store](https://apps.shopify.com/aivastra)
- Neither vendor's page states an offline mode, a maintenance schedule, or an SLA/uptime commitment (confirmed absence from both listings).
- One general industry source notes that "most VTO [virtual try-on] processes do not store images and operate on data locally on the device" as a vendor claim for some virtual-try-on products generally — but this was not confirmed for Looksy or AI Vastra specifically, and is contradicted by both tools' evident server-side/credit-metered processing model — [Glamar — Virtual try-on mirror](https://www.glamar.io/solutions/vto/virtual-try-on-mirror)

### Inferences
- Both tools require reliable store-side internet connectivity (Wi-Fi/broadband) to function at all — there is no offline fallback implied anywhere in either vendor's materials. For the Premium Lounge in Jalpaiguri, this means internet reliability (not just tablet hardware) is a dependency for the try-on experience to work at all; a backup connectivity plan (e.g., 4G/5G dongle failover) would be a sensible mitigation.
- Software updates are most likely handled entirely vendor-side (standard for a SaaS widget/app) — no local software maintenance burden is implied beyond keeping the tablet's browser/OS and the Shopify theme up to date.
- Running out of credits (both tools use consumable credit models) is an ongoing *operational* cost to budget and monitor, not a one-time setup cost — this is a recurring line item to factor into Ma Lakhsmi Stores' running costs, distinct from the one-time tablet hardware purchase.

### Gaps
- No published SLA, uptime percentage, or formal maintenance/update cadence from either vendor.
- No information on what happens to the try-on feature during an internet outage (e.g., graceful degradation vs. hard failure) — not stated by either vendor.
- No data-retention/privacy-policy specifics were retrieved for either tool (both pages referred to separate privacy policy documents not fetched in this pass) — relevant given India's data protection rules on customer photo capture, flagged here as a compliance gap to check before launch.

---

## Overall Summary Table (for the report writer)

| Dimension | Looksy AI | AI Vastra |
|---|---|---|
| Actual product type found | Shopify/web e-commerce try-on widget (photo upload) | Shopify app (photo upload), by Nice Interactive (Rajahmundry, AP, India) |
| Dedicated in-store/tablet kiosk product? | Not found/confirmed | Not found/confirmed |
| Stated device specs | None ("works on all devices and screen sizes") | None published |
| Special hardware (depth sensor, body scan, camera rig) | Not required/mentioned | Not required/mentioned |
| Setup process | Vendor-assisted, no-code, ~1 business day, multiple e-commerce platforms supported | Standard Shopify app install; no stated timeline |
| POS/inventory integration (Marg ERP, Zoho Inventory) | None found | None found |
| Connectivity/offline | Cloud/credit-based, implies mandatory internet, no offline mode stated | Cloud/credit-based (one-time credit packs), implies mandatory internet, no offline mode stated |
| Pricing model | Subscription + credits (e.g., $169/mo tier with 1,500 credits seen on one listing) | One-time credit packs: Free (25 credits/5 try-ons) to Platinum ($100/10,000 credits/2,000 try-ons) |
| Launched | App listing seen; per one source, Dec 12, 2025 | Aug 24, 2026 (Shopify listing), no reviews yet |

**Biggest flag for the report:** Neither product, as found in open research, is documented as an in-store tablet-kiosk product — both are e-commerce storefront widgets. Before buying tablets or committing the Premium Lounge build-out around these two specific brand names, Soumyanil should verify directly with each vendor whether an in-store/kiosk deployment mode exists, or consider comparison with vendors that explicitly do in-store tablet/kiosk deployments in India (e.g., Trupik, DaveAI/Tanishq-style avatar showrooms, PointAI), none of which were the specific assignment scope here but surfaced as relevant alternatives during research.
