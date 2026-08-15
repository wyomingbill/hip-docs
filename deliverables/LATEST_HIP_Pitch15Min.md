# HIP — The 15-Minute Version

Status: BUILT
Reconciled-Against: roadmap 3239ff8 (2026-08-05)
Prepared-By: Claude (Opus 5)
Verification: STATUS-LABELS RECONCILED TO §16 AS OF 2026-08-05; narrative unverified

A timed script, not a summary. Every topic from the full pitch appears; the detail is stripped and the breaking points are not. Roughly 2,000 spoken words.

**Two rules that survive compression:** plain English only, and never blur what's proven with what isn't. Compression is where those go first. Each block below carries its status label — say it.

Cut list at the bottom: what was dropped, and where to reach if someone asks.

---

## 0:00 — THE CLAIM *(60 seconds)*

Most AI products tell the AI "don't share that." We don't give it to the AI in the first place. **A model cannot decline to reveal what it never saw.**

Everything I'm about to say is evidence we actually did that. Every company in this category writes instructions telling the model what not to say — that's asking a very persuadable thing to keep a secret. It works most of the time, and most of the time is a rounding error away from a headline.

We're not claiming our AI is better behaved. We're claiming we removed the opportunity to misbehave.

---

## 1:00 — NEED TO KNOW *(2 minutes 30)*

There's a discipline that already solved this, and it didn't solve it with rules about behavior.

In the intelligence world, a clearance does not get you information. A clearance means you've been vetted; it says nothing about what you're entitled to see. Access needs a second, separate thing: **need to know.** Material is divided into compartments, and getting into one is a deliberate act by someone with the authority to do it. You are *read in* — told what it covers, told the rules, signed for. Your name is on a list. You can be *read out.*

Two things follow, and they're what this company is built on.

**Clearance is not access.** The most cleared person in the building can't enter a compartment they have no need to know about. Rank doesn't do it. Seniority doesn't do it. And this is the one that matters: *asking nicely doesn't do it, and neither does volunteering.* You can't talk your way into a compartment by being agreeable or by already being in four others.

**Enforcement is at the door, not at the mouth.** Nobody hands a cleared officer the whole file and asks them to be careful about which parts they discuss. The material they don't need never enters the room.

**The argument, as strongly as I'll make it:** compartmentalization is the only approach to sensitive information that has ever worked at scale, and it works because it doesn't depend on the discretion of the person holding it. Everything else — rules, training, review — is a filter applied after someone already has the material. Filters fail open. A compartment fails toward less.

The translation is nearly one-to-one. Being an adult in the household is a clearance, not access. Being an enrolled caregiver is a clearance, not access — it gets you the compartments your care role requires. A daughter managing medications is read into medications. That doesn't read her into her father's finances, however trusted and present she is.

And the sharpest version: **the AI is read in per question and read out when the question ends.** Not a cleared employee with standing access — a contractor brought into one compartment for one meeting, handed exactly what that meeting requires, walked out. The next question is a fresh read-in. It never accumulates.

> **Say these yourself.** Compartments are famously why nobody connected the dots before 9/11 — which is exactly why our care facts default to visible across the whole enrolled care team rather than private to whoever wrote them. Between a failure that's embarrassing and one that's medical, we take the embarrassing one. Second: need-to-know never solved the insider with legitimate access. It shrinks the blast radius. Third: being read out is a signature on a form, not a technical control — we stop future access and rotate keys; we cannot make anyone unremember.

*Per-question read-in: **proven.** Reading a new caregiver into current-but-not-historical material: **specified, not built.***

---

## 3:30 — THE MACHINE, IN TEN STEPS *(2 minutes 30)*

Walk this slowly. It's the clearest minute in the pitch.

A daughter says: *"Dad's been forgetting his evening pills."*

**Voice** takes it in and hands over words. It holds no key and cannot write to memory. **The listener** — a small model on the box — proposes a fact. It proposes; it doesn't commit. **The labeler** tags it at the door: how sensitive, who may see it, whether it may ever leave the house. If the label can't be determined, it's refused, not guessed. **It's sealed** to the keys of the people entitled to it. **It enters as a claim, not a fact,** because it's about someone else — Dad or his custodian confirms it before it hardens. **The record is written** and its head is signed and copied somewhere the system cannot reach or alter.

Later the other daughter asks whether Dad's doing okay with his medications. **The read-in happens** — a folder assembled for her specifically. **Routing decides** whether this is answerable on the box or needs an outside service, and what may cross that line. **The model gets the folder** and answers from it; empty folder means it says so and stops rather than constructing something plausible. **The decision is recorded**, and afterward you can check whether the refusal was structural or the model just being cautious.

**Nine of those ten steps happen whether or not the model behaves well.** That's the architecture.

**Two things about the models, since everyone asks.** We didn't train any of them — we rent them all. And there is a layer that finds patterns across what a household has told us, which I will not call a learning layer, because nothing here learns. No weights change because you used it. Call it the pattern layer.

The pattern layer is obviously the most dangerous component in the building, so: it needs two supporting facts and must name them; anything it produces is low-confidence and **cannot promote its own guesses** — only a human confirming can; take away a supporting fact and the conclusion dies with it. And it doesn't see what anyone said. It gets the *kinds* of facts and how well established they are, never the values. It can see there's a medication fact, an incident, and an appointment about the same person in one fortnight. It cannot read what the medication is.

> **Breaking point:** the shape is often enough. Three medication facts and a cardiology appointment in a fortnight tells you plenty without a single value. That's a real narrowing. It is not blindness.

*Pattern-layer constraints and retraction-kills-the-conclusion: **proven.** The limits on what *kind* of conclusion it may draw: **proven** — with two of the four parts holding because we read sixteen files and found no code that does the forbidden thing. **That's absence verified, not a guard on duty.** The watcher that would catch someone writing that code later is authorized and not built.*

---

## 6:00 — THE BUG WE FOUND *(3 minutes — the credibility moment)*

A daughter tells the system her father has been hiding how much he's drinking.

That fact gets a sensitivity label, and the label decides who sees it and whether it may leave the house. The code checked the label against a list of known labels. If it wasn't on the list, it filled in "medium" and carried on.

Medium is allowed to leave the house.

So the most private thing anyone in that family said that month gets packaged up and sent to an outside AI company. No error, no alert. **Three separate places did this, and every one failed toward permitting.**

A bouncer who lets you in whenever he can't read your ID. Not lazy — he was told to keep the line moving, and nobody comes back to complain that they got in.

> **Breaking point:** a bouncer's mistake is over by morning. A leak is invisible and permanent. And someone told that bouncer to keep the line moving. That someone was us.

**Why it survived, and this generalizes past us:** a failure that *blocks* something gets a phone call in ten minutes. A failure that *permits* something gets found years later by a journalist. Every incentive in software finds the first kind fast and the second kind never. Ask any company that claims to protect data what they found when they went looking for permissive failures. Most have never looked, because nothing was broken.

**The fix:** all three refuse instead of guessing, and we removed the ability to set a fallback entirely. Every safety valve we ever built with a default in it eventually became a silent downgrade. The option isn't available to us anymore either.

**Then we went looking for the same disease elsewhere and found it.** We have six kinds of records the system will never store. One no longer has a working check behind it — not because anyone decided it was acceptable, but because the check needs to recognize who a fact is about, and it doesn't recognize "Dad" or "the household" as identities. It couldn't do its job, so we pulled it rather than let it pretend. Nothing reaches it today; it arms the first time a genuine outsider enters the picture. Written down, assigned, held by a standing test.

I'm telling you that because you were about to ask "so nothing mislabels anymore?" — and you'd have had it out of me in one question. Anyone can say their system is careful. Almost nobody tells you what they found when they went looking.

*The fix: **proven.** The second hole: **known, open, bounded.***

---

## 9:00 — HOW IT'S STORED, AND WHAT LEAVES *(2 minutes 30)*

Three things, quickly, and I'll give you the limit on each.

**Every fact is a sealed envelope with a readable outside.** Contents encrypted; the label — who, about whom, what kind, how sensitive, when — is not, because otherwise nothing could be found without opening everything. The search index is built only from those labels, never from what was said. **The cost, stated:** someone reading only labels still learns your father has twelve medication facts and four fall-related facts. The shape of a life shows even when the contents don't. Anyone claiming they encrypt everything and still search instantly is describing something that doesn't exist.

**The master key.** We started with one key on the same machine that could open every fact in the house. We rebuilt it — facts are now sealed to individual people's keys, and the old path can no longer derive anyone's key anywhere it used to. The key still exists on that machine. Until it's destroyed, the honest sentence is "the operator can't reach your facts through the old path," not "the operator can't reach your facts." And when we went to destroy it, we found the code silently mints a new one the instant the file goes missing. So "destroyed" isn't currently a state this system can be in. We found that by trying, not by reading the design.

**The limit that doesn't go away.** To answer a question, facts have to be decrypted into working memory. Someone with full control of that machine, at that moment, could read that turn. Closing it needs hardware that encrypts memory even from the machine's owner. We don't have it and we're not planning around it. An outside security review reached the same conclusion independently and named the same fix we'd already ruled out of scope.

**And what leaves.** Some questions are answered on the box; some go to an outside AI service, and sensitivity decides which — the most sensitive facts never leave regardless of what's being asked. We have a mechanism that strips household facts from outbound requests and **it does not cover every path.** Found, filed, open decision. Not fixed today.

> **Breaking point:** removing the name doesn't remove the story. Stripping identifiers is the weak control. The strong one is the fact not being eligible to leave at all.

*New locks: **proven.** Key destruction: **built, not run,** with a blocker we found ourselves. Outbound stripping: **built with a known gap.** Protection while answering: **out of scope by decision.***

---

## 11:30 — WHAT WE DIDN'T BUILD *(1 minute 30)*

We build the memory, the governance, the assembly of what goes into any given question, and the record that proves it. We rent the models, the speech, the databases, the hardware. **Models commoditize; governed memory compounds.**

And here's the list I'd want from anyone claiming what we claim — **what we deliberately did not build.** Protection at the moment of answering. Always-on ambient voice. Any system that learns from your household. The assistant deciding on its own to start conversations. Each is written down with the reason.

**One item moved off that list recently, and I'll say exactly how far it moved.** Erasure — removing a fact, or everything about a person — is now built and proven against test fixtures, with a machine-checkable report of what came out. **And nothing in the live system can invoke it from a real request, nothing real has ever been erased, and anything written before the rebuild stays unerasable forever.** I am not telling you we can delete your data. I'm telling you the machinery exists, is proven where we could prove it, and isn't connected to anything a person can press.

Two are positions rather than queue items. **Retrieval stays rule-based indefinitely** — a rule can be audited, a learned ranker can't, and auditability *is* the product claim, so we don't get to trade it for relevance. And **ambient listening stays off** until the collection limits underneath it are proven; an always-listening device with unproven limits is precisely the product we're arguing against.

**One thing I'd put weight on:** before building any learning component, we built the check that would catch a bad one — a validator that refuses any training example crossing between households or between people who shouldn't share a signal. Wired at the strictest tier, tested by deliberately feeding it violations. **It's guarding nothing, because there's no learner.** We built the fence before we got the animal.

> **Breaking points:** rule-based retrieval will be worse at finding the right six facts — I'm buying explainability with a quality ceiling, and that's a legitimate thing to disagree with. And a fence proves nothing about an animal that doesn't exist; the real test is the day someone finds it easier to move the fence than fix the learner.

**The other thing we won't do:** the asking problem. Every product on earth measures the percentage of people who say yes and tries to raise it — and once that number is a target, every dark pattern follows automatically, with nobody having to be a villain. Yes to pill reminders becomes yes to location becomes yes to sharing sleep patterns with your sister, each yes the argument for the next, and nobody ever asks the real question because on day one you'd say no. Our answer: ask only when something in the world actually changed, once per situation, wording from fixed templates the AI can never tune, and a decline is never a fact about you. **Say the split precisely: the rules are real code and the behavior is nothing.** What counts as a reason to ask, what explicitly doesn't count, and the gate allowing one offer per situation are built. **Nothing in the live system can make an offer at all**, and none of the four kinds of real-world change can be represented yet. If anyone hears "they shipped ethical consent," I've said it wrong.

---

## 13:00 — THE ADVANTAGE, AND THE HONEST NUMBER *(1 minute 30)*

**The unit of protection is the household, not the user.** Every assistant on the market is built for one person with one account. A house has people whose interests genuinely conflict. That's where eldercare actually lives and nobody's building for it.

**The record is the product.** Every decision written as it happens, copies beyond the system's reach — so a skeptical engineer can be handed this and told to break it, and "did it really refuse for the reason you claim" is checkable rather than asserted.

**And the argument against my own case**, which I'd rather make than have made at me: that's engineering discipline, not invention. A funded team could copy it in eighteen months. Most won't, but "most won't" isn't a moat. The durable advantage is the accumulated governed history of a household — which nobody can buy and nobody can lawfully train on — and that requires being in the house long enough for it to accumulate. That's a distribution problem, not a technology problem. **If someone tells you their AI privacy architecture is a moat, they're selling.**

**The number I lead with:** thirty requirements, eleven proven, none failing, nineteen never had their test run — and most of those nineteen can't run, because the thing they'd test isn't built. That doesn't say we're a third done. It says we have a system that tells us what we haven't proven. Most teams can't produce that number — not because it's zero, because nobody's counting.

> **Breaking point, both directions.** Nineteen unrun tests isn't nineteen broken things — it's a count of missing proof, not defects. **And "none failing" is not "nothing wrong."** It means nothing sits in the failed column on that board. There are known defects and known debt underneath it, several of which I've already named tonight. Letting you hear "none failing" as "nothing wrong" would be the exact thing this whole talk argues against.

---

## 14:30 — CLOSE *(30 seconds)*

> Some of what I've described is proven — tested and formally accepted. Some is built and running and we have not accepted the proof. Some is written down and not built. And some we've decided not to do at all, and I'll tell you why for each one. You'll get told which of those four you're looking at every single time you ask.

Stop there. Don't add.

---

## CUT LIST — what's not in the 15-minute version

If asked, these are in the full pitch and you can go to them:

- **The four governance pieces as separate ideas** (briefing packet, nurse's license, evidence room, pharmacist). Folded into the need-to-know frame and the ten-step trace. The nurse's-license line is the one worth keeping in your pocket: *consent does not expand scope — a patient cannot authorize their nurse to perform surgery.*
- **The keyless person and the two-person key structure.** Reach for it the moment anyone asks how an 80-year-old without a phone is protected. Includes why care-team-visible is the deliberate default.
- **Voice as permanently untrusted**, and the honest note that the current deployment runs voice in the same process that can write to memory.
- **The five modes of communication** and why only two are live.
- **The first-conversation onboarding** — designed, no requirement written, no code.
- **Multi-tenancy** — why memory-encrypting hardware does not separate one household from another, and why many private models on one chip is not offered.
- **The order-window property** — households never touch the AI service directly, which breaks a published attack architecturally.
- **The confirmation channel** that no model output can reach. This is the one piece a patent attorney would look at twice. *Verify its current wiring before claiming it.*
- **The write-side gap** — governance controls what models see; the path where model output causes a write lacks the same authority check. Filed, known, open. Volunteer it if the room is technical.
