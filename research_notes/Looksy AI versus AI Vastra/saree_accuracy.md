# Looksy AI vs. AI Vastra — Saree/Ethnic Wear Try-On Capability

**Important naming caveat found during research:** Both product names are ambiguous online. There are at least three distinct entities trading under "Looksy AI"/"Looksy," and at least two under "AI Vastra"/"Vastra AI." Findings below are kept separated by which specific entity they came from so the report writer can flag this disambiguation risk to Soumyanil before he commits to either vendor.

- "Looksy AI Virtual Try-On" — a Shopify app, developer address given as San Francisco, CA, US. ([Shopify listing](https://apps.shopify.com/looksy))
- "Looksy.tech" — a separate company based in Dubai Silicon Oasis, UAE, founded by Kirill Pegov and Natalia Varga, combining an AI try-on widget with an AI shopping assistant. ([SaaSHub](https://www.saashub.com/looksy-tech), [Looksy About Us](https://looksy.tech/about_us))
- "Looksy AI Outfit Changer" — a separate consumer app listed on Product Hunt/hunted.space for casually changing outfits in photos. ([hunted.space](https://hunted.space/product/looksy-ai-outfit-changer))
- "Ai Vastra: Virtual Try-On" — a Shopify app. ([Shopify listing](https://apps.shopify.com/aivastra))
- "AI Vastra" (aivastra.com) — an Indian company, powered by "Nice Digitals," based in Surat, Gujarat, offering AI virtual try-on, AI-generated catalogues, and retail kiosk solutions. This is almost certainly the entity behind the Shopify app above, and is the one most relevant to Soumyanil's use case (in-store kiosk for an Indian saree retailer). ([aivastra.com](https://aivastra.com), [job listing describing the company](https://jobs.weekday.works/product-marketing-executive-at-ai-vastra-wkdyhzl2g0))
- A separate "Vastra AI" is an unrelated outfit-recommendation chatbot, not a try-on visualizer — not relevant here. ([topai.tools](https://topai.tools/t/vastra-ai))

---

## Does Looksy AI explicitly support saree/ethnic Indian wear try-on, or is it primarily built for Western/stitched garments? How accurate is drape/pleats/pallu rendering if demoed/reviewed?

### Takeaway
No evidence was found that any "Looksy AI" entity explicitly supports sarees or Indian ethnic wear, or that it has been demoed/reviewed on saree draping, pleats, or pallu accuracy. All available marketing material describes generic "clothing," "outfits," and stitched-garment categories (plus eyewear/jewelry/accessories), with no mention of India, sarees, or unstitched/draped garments anywhere.

### Cited Findings
- The Looksy AI Virtual Try-On Shopify listing describes the app as suited to "fashion, accessories, and jewellery" broadly, with shoppers clicking "Try On," uploading a photo, and getting an instant preview — no saree or ethnic-wear category is named. — [Shopify app listing](https://apps.shopify.com/looksy)
- Looksy.tech's own "About Us" page lists supported categories as "Clothing, eyewear, jewelry, and bags & accessories. More categories coming soon," with no breakdown of garment types and no mention of saree, sari, India, ethnic wear, blouse, drape, pleats, or pallu anywhere on the page. — [Looksy About Us](https://looksy.tech/about_us)
- Looksy.tech is based in "Dubai Silicon Oasis, Dubai, United Arab Emirates," per its own About page — no stated India presence, office, or market focus. — [Looksy About Us](https://looksy.tech/about_us)
- The Looksy AI Virtual Try-On Shopify listing shows only 3 visible reviews (out of a reported low total), from stores named palmer//harding and Shadesbywoodpecker (both apparently UK-based) and TinyBlues (Pakistan) — none are Indian or ethnic-wear/saree retailers, and none of the visible review text references garment type or drape accuracy. — [Shopify app listing](https://apps.shopify.com/looksy)
- A separate "Looksy AI Outfit Changer" listing (Product Hunt/hunted.space) describes only generic "outfit changes" and "fashion transformations," and the developer explicitly invites users to request "what outfit styles should we add," implying the current supported style range is limited and does not already include saree/ethnic wear. — [hunted.space](https://hunted.space/product/looksy-ai-outfit-changer)

### Inferences
- Because none of the three "Looksy" entities mention India, sarees, or draped garments anywhere in their own marketing copy, the product line (whichever entity is meant) was very likely designed and validated primarily against Western, stitched (sewn-to-shape) garments — shirts, dresses, jackets — where a 2D/3D fit model can rely on consistent seams and silhouette. A 5.5-meter unstitched draped fabric with pleats and a free-hanging pallu is a fundamentally different rendering problem (no fixed seams, drape physics vary by fabric and draping style), and there is no claim anywhere that Looksy's model was trained or tested for this.
- The lack of any demo, screenshot, or review showing saree try-on suggests this is a genuine capability gap rather than an omission in marketing copy, but it cannot be ruled out that a demo exists that simply didn't surface in search.

### Gaps
- No demo video, screenshot, or third-party review showing any "Looksy AI" entity rendering a saree, pleats, or pallu was found. This could mean the capability does not exist, or that a private/unindexed demo exists — contacting Looksy directly (a free demo is offered per its FAQ) would be the only way to confirm either way.
- Could not determine with certainty which "Looksy AI" entity (San Francisco Shopify app vs. Dubai looksy.tech vs. the Outfit Changer app) is the one referenced in Soumyanil's context files — this should be clarified before any purchase decision.
- No information found on Looksy's underlying rendering technology (diffusion-based image generation vs. 3D garment simulation), which would affect how it would plausibly handle draped fabric even in an untested scenario.

---

## Does AI Vastra explicitly support saree try-on, and how accurately does it render drape, pleats, and pallu?

### Takeaway
AI Vastra (aivastra.com, Surat-based, "powered by Nice Digitals") explicitly and prominently markets saree/ethnic-wear try-on as a core use case and claims to be "specifically trained on Indian garment types," including realistic draping — but it gives no verifiable accuracy data, and neither pleats nor pallu are mentioned anywhere on its own site, so drape quality on those specific details is unconfirmed.

### Cited Findings
- AI Vastra's site states the try-on feature is "especially useful for sarees, bridal wear, and ethnic fashion," where drape on a specific body matters, and says the AI "understands how traditional fabrics fall on a body." — [aivastra.com](https://aivastra.com)
- The site's FAQ lists supported garment categories as "sarees, lehengas, salwar kameez, kurtas, sherwanis, and bridal wear" (plus Western categories: dresses, tops, shirts, trousers, and men's/children's/accessories), and states the model is "specifically trained on Indian garment types." — [aivastra.com](https://aivastra.com)
- The companion Shopify app listing ("Ai Vastra: Virtual Try-On") states under features: "Indian & Western Wear: Supports sarees, kurtas, lehengas, shirts, dresses & more" and "Realistic Drape: See how outfits naturally look and drape on the customer." — [Shopify app listing](https://apps.shopify.com/aivastra)
- The aivastra.com homepage displays an unsourced claim of "100% Design Accuracy" with "Consistent colours, fit, and styling every time" — no methodology, test set, or third-party verification is given for this figure. — [aivastra.com](https://aivastra.com)
- Neither "pleats" nor "pallu" appears anywhere on the aivastra.com site or the Shopify listing in the content retrieved. — [aivastra.com](https://aivastra.com); [Shopify app listing](https://apps.shopify.com/aivastra)
- The Shopify app listing for "Ai Vastra: Virtual Try-On" shows 0 ratings and "No reviews yet," so there is no independent review evidence (positive or negative) on actual rendering quality. — [Shopify app listing](https://apps.shopify.com/aivastra)
- A job posting for AI Vastra (recruiting a product marketing executive) independently describes the company as "powered by Nice Digitals," based in Surat, Gujarat, offering "AI virtual try-on, AI-generated catalogues, and retail kiosk solutions" aimed at "garment manufacturers, brands, retailers, and ecommerce sellers" across Surat — this is a self-description via a recruiting listing, not independent journalism, but it corroborates the company's own site. — [Weekday job listing](https://jobs.weekday.works/product-marketing-executive-at-ai-vastra-wkdyhzl2g0)

### Inferences
- AI Vastra is clearly positioned, by its own marketing, as an Indian-ethnic-wear-first product (saree/lehenga/sherwani/bridal front and center, Western wear listed second) — a meaningfully different positioning from the generic "Looksy" entities. For a saree retailer, this alone makes AI Vastra the more aligned product on paper.
- However, "100% Design Accuracy" with no methodology is a marketing claim, not evidence, and the complete absence of "pleats" or "pallu" as explicit terms on the vendor's own site — even though these are the hardest parts of saree draping to get right — suggests the vendor has not specifically validated or marketed around these sub-components. This doesn't necessarily mean the rendering is poor, but it means there's no vendor-provided evidence either way on the specific details Soumyanil cares about.
- Zero Shopify reviews and no found case studies means AI Vastra's saree-specific claims are currently unverified by any independent party.

### Gaps
- No independent review, demo video, or screenshot showing actual saree drape/pleat/pallu rendering quality from AI Vastra was found or retrievable — the site references a "Watch a Demo" button, a YouTube channel, and a "Case Studies" page, but the actual video/case-study content was not retrievable in this research pass and should be checked directly (aivastra.com) or requested via their "Book A Free Demo" CTA.
- No methodology or sample size behind the "100% Design Accuracy" claim could be found.
- No press coverage (Economic Times, YourStory, Inc42, or similar) on AI Vastra/Nice Digitals was found — this is a gap, not a confirmed absence of coverage (the company may simply be too early-stage/under-the-radar to have been covered, or coverage may exist under the "Nice Digitals" parent name rather than "AI Vastra").

---

## Is blouse try-on (separately from the saree drape itself) supported by either product?

### Takeaway
No evidence was found that either Looksy AI (any entity) or AI Vastra explicitly supports blouse try-on as a distinct, separate step from the saree drape itself. This is a clear capability gap in the available marketing material for both products.

### Cited Findings
- Neither aivastra.com nor the "Ai Vastra: Virtual Try-On" Shopify listing mentions "blouse" anywhere in the retrieved content. — [aivastra.com](https://aivastra.com); [Shopify app listing](https://apps.shopify.com/aivastra)
- Neither the Looksy AI Shopify listing nor the Looksy.tech About Us page mentions "blouse" anywhere in the retrieved content. — [Shopify app listing](https://apps.shopify.com/looksy); [Looksy About Us](https://looksy.tech/about_us)
- By contrast, a Google Cloud-built internal tool for Meesho (a different, unrelated e-commerce company, surfaced only as context) explicitly separates the blouse image from the saree body and pallu images as three distinct inputs when generating saree try-on visuals — showing that treating blouse as a separate component is technically established practice elsewhere in the Indian saree-tech space, even though it isn't confirmed for either of our two target products. — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/virtual-try-on-technology-with-google-cloud-ai) (found via search snippet; not independently fetched/verified in full)

### Inferences
- The absence of "blouse" as a marketed feature for either product likely means blouse try-on, if it works at all, is not a distinguished/separately-validated feature — it would presumably just be rendered as part of whatever single saree image or outfit image is uploaded/generated, with no dedicated blouse-swap or blouse-only preview capability advertised.
- Given that blouse design/color/neckline is often the single biggest customization decision a saree buyer makes in-store (blouse is frequently stitched separately from the saree), this is a meaningful functional gap for Soumyanil's in-store kiosk use case if neither vendor has it — worth asking both vendors directly in a demo call.

### Gaps
- Could not confirm from public sources whether either vendor's underlying product (behind the marketing page) actually supports a blouse-specific try-on workflow — this would require a live demo/sales call with each vendor, since product pages are necessarily incomplete feature lists.

---

## Are there demo videos, screenshots, or customer testimonials from Indian ethnic-wear/saree retailers using either product, and what do they say about visual realism/accuracy?

### Takeaway
No customer testimonials, case studies, or independently viewable demo content from Indian ethnic-wear or saree retailers were found for either product. AI Vastra's homepage names large brand logos ("Trusted by Leading Brands": Myntra, Mirraa, Dalmia) but with no attributed quotes and no saree-specific context; Looksy has zero Indian-retailer reviews of any kind.

### Cited Findings
- AI Vastra's homepage displays brand logos including Myntra, Mirraa, and Dalmia under a "Trusted by Leading Brands" banner, and a "Results That Speak" section with unlabeled before/after-style images, but no attributed customer quotes and no saree-specific case study text was retrievable. — [aivastra.com](https://aivastra.com)
- An aivastra.com footer links to a dedicated "Case Studies" page, but its content was not retrievable in this research pass (link present, content not loaded/indexed at time of search). — [aivastra.com](https://aivastra.com)
- The "Ai Vastra: Virtual Try-On" Shopify listing shows 0 ratings / "No reviews yet," so there are no Shopify-verified merchant reviews at all. — [Shopify app listing](https://apps.shopify.com/aivastra)
- The Looksy AI Virtual Try-On Shopify listing's visible reviews come from a UK-based lingerie/clothing brand (palmer//harding), a UK sunglasses-adjacent brand (Shadesbywoodpecker), and a Pakistan-based store (TinyBlues) — none are Indian, and none are saree/ethnic-wear retailers. — [Shopify app listing](https://apps.shopify.com/looksy)

### Inferences
- The "Trusted by" Myntra/Mirraa/Dalmia logos on AI Vastra's site, if accurate, would be a meaningful signal (Myntra in particular is a major Indian fashion e-commerce player) — but since this is unattributed logo-dropping with no case study, quote, or saree-specific context, it cannot be verified or treated as confirmed evidence of saree-try-on performance specifically (these brands could be using AI Vastra for Western wear, or the logos could be aspirational/unverified marketing).
- The complete absence of any Shopify reviews for the Indian-market-focused "Ai Vastra" app, versus even a handful for the Western-market "Looksy" app, suggests AI Vastra may be earlier-stage / have fewer live merchant installs via that channel (though its primary sales motion may be direct/kiosk rather than Shopify app-store discovery, per the Surat-focused recruiting listing).

### Gaps
- No case study, demo video, or testimonial specifically describing saree drape/pleat/pallu realism from any real retailer's experience was found for either product. This should be treated as a clear "no evidence found" rather than assumed to be positive or negative — Soumyanil should request specific saree-garment demo footage and ask for reference-customer contacts directly from both vendors before purchasing.
- Could not verify whether the Myntra/Mirraa/Dalmia logos on AI Vastra's site represent active paying customers, pilot users, or unauthorized/aspirational logo use.

---

## Which product (if any) markets itself specifically toward Indian ethnic wear/saree retailers versus general fashion retailers?

### Takeaway
AI Vastra (aivastra.com) clearly and specifically markets toward Indian ethnic wear — it is based in Surat (India's textile/garment hub), leads with saree/lehenga/bridal/sherwani language, and claims Indian-garment-specific training. None of the "Looksy AI" entities show any India or ethnic-wear-specific positioning; all describe themselves in generic global-fashion/Western-garment terms.

### Cited Findings
- AI Vastra's FAQ explicitly states its model is "specifically trained on Indian garment types," listing sarees, lehengas, salwar kameez, kurtas, sherwanis, and bridal wear ahead of Western categories. — [aivastra.com](https://aivastra.com)
- A recruiting listing for AI Vastra describes its sales motion as targeting "garment manufacturers, brands, retailers, and ecommerce sellers" specifically "across Surat" — i.e., embedded in India's garment-manufacturing ecosystem, not a generic global SaaS play. — [Weekday job listing](https://jobs.weekday.works/product-marketing-executive-at-ai-vastra-wkdyhzl2g0)
- Looksy.tech's own About Us page gives its location as Dubai and lists only generic "Clothing, eyewear, jewelry, and bags & accessories" categories with no India or ethnic-wear mention. — [Looksy About Us](https://looksy.tech/about_us)
- The Looksy AI Virtual Try-On Shopify app's visible merchant base (UK, Pakistan) and generic "fashion, accessories, and jewellery" framing shows no Indian-market or ethnic-wear-specific positioning. — [Shopify app listing](https://apps.shopify.com/looksy)

### Inferences
- On positioning/marketing alone, AI Vastra is the more natural fit for an India-based saree retailer's kiosk use case — it is literally built in India's garment hub and leads with the exact garment categories Soumyanil's store needs. Looksy's products (whichever entity) show no evidence of having considered draped/unstitched Indian garments at all in their design.
- This is a positioning/marketing conclusion, not a proven accuracy conclusion — AI Vastra's "specifically trained on Indian garment types" claim and "100% Design Accuracy" claim remain unverified by any independent source (see above). Soumyanil should treat AI Vastra as the more promising candidate to pilot/demo first, but should not assume its marketing claims equal validated real-world accuracy without seeing a live saree demo himself.

### Gaps
- No side-by-side comparison, independent benchmark, or review site that directly pits "Looksy AI" against "AI Vastra" on saree rendering was found — this comparison appears to not exist publicly and would need to be generated by Soumyanil requesting live demos from both vendors using his own store's sarees.

---

## Adjacent context (not the assigned products, but relevant for the report writer / decision-maker)

While researching, several *other* tools surfaced that are explicitly saree-draping-specific and may be worth the report writer flagging as alternatives or benchmarks, since neither primary subject has demonstrated comparable saree-specific depth:

- **VaBhu / SareeXchange** — described as draping a saree onto a single uploaded selfie via AI in seconds, with video previews of drape and flow. — [search snippet, not independently verified by direct fetch]
- **Meesho (with Google Cloud)** — built an internal saree try-on tool that generates 2D images and 3D models from three separate inputs: a blouse image, a saree body image, and a pallu image — notable as a precedent for treating blouse/body/pallu as distinct components. — [Google Cloud blog](https://cloud.google.com/blog/products/ai-machine-learning/virtual-try-on-technology-with-google-cloud-ai)
- **Perfect Corp YouCam API** — offers a "Try On Indian Sari" API feature for developers. — [Perfect Corp](https://yce.perfectcorp.com/ai-api/contents/sari)
- **Drapis** — a wardrobe-styling app stated to be "designed especially for Indian wardrobes with full support for sarees, kurtas, lehengas, sherwanis." — [search snippet; not independently verified by direct fetch]
- An academic paper (Journal of Advances in Information Technology, 2025) describes a smart-mirror system using AR/AI to drape sarees in real time for in-store shopping — relevant as a sign that real-time in-store saree-draping tech is an active research area, separate from either Looksy or AI Vastra. — [BCU open-access repository](https://www.open-access.bcu.ac.uk/17060/)

None of these were deeply researched (out of scope per the assignment), but their existence suggests saree-specific try-on technology is achievable and being built by multiple parties — which is useful leverage for Soumyanil when evaluating/negotiating with Looksy AI or AI Vastra, or as fallback options if neither primary candidate's live demo proves convincing on pleats/pallu/blouse specifically.
