# HIP — The Full Pitch (v2)

Status: BUILT
Reconciled-Against: roadmap 3239ff8 (2026-08-05)
Prepared-By: Claude (Opus 5)
Verification: STATUS-LABELS RECONCILED TO §16 AS OF 2026-08-05; narrative unverified

Supersedes v1. v1 covered governance and the two stories only. This version adds the four things a technical room actually asks about — how it's stored, what leaves the house, what it feels like to use, and where the borders are — plus a straight answer on what the real advantage is.

Plain English throughout. Every analogy has its breaking point written underneath it. Say the breaking point yourself, before someone in the room finds it.

Three claims are kept apart everywhere: **designed**, **built but not proven**, and **proven**. The recap at the bottom repeats the whole split.

---

## PART ONE — THE CLAIM

### 1. THE OPENING SENTENCE

> Most AI products tell the AI "don't share that." We don't give it to the AI in the first place. A model cannot decline to reveal what it never saw.

Everything after this is evidence that we actually did it.

### 2. WHY THAT DISTINCTION IS THE WHOLE COMPANY

Every AI privacy story you've heard works the same way: the company writes instructions telling the AI what not to say. That's asking a very persuadable thing to keep a secret. It works most of the time, which is the problem — most of the time is a rounding error away from a headline.

We built the other version. Before the AI is asked anything, something decides what it's allowed to see and hands it a smaller set of facts. The AI doesn't refuse. It answers honestly from what it has, and what it has doesn't include your father's drinking.

**Say it out loud:** we are not claiming our AI is better behaved. We're claiming we removed the opportunity to misbehave.

### 3. THE FRAME — NEED TO KNOW, AND BEING READ IN

*(This is the master frame. Everything in Parts Two through Five is an instance of it. If the room only takes one idea away, take this one.)*

There's a discipline that already solved this problem, and it didn't solve it with rules about behavior.

In the intelligence world, having a clearance does not get you information. A clearance means you've been vetted. It says nothing about what you're entitled to see. Access requires a second, separate thing: **need to know.** Sensitive material is divided into compartments, and getting into one is a deliberate act performed by a person with the authority to perform it. You are *read in* — told what the compartment covers, told the handling rules, signed for. Your name is on a list. You can be *read out* the same way.

Two things follow from that structure, and they're the two things this whole company is built on.

**First: clearance is not access.** The most cleared person in the building still cannot walk into a compartment they have no need to know about. Rank doesn't do it. Seniority doesn't do it. And — this is the important one — *asking nicely doesn't do it, and neither does volunteering.* You cannot talk your way into a compartment by being agreeable, by being around a long time, or by already being in four other compartments.

**Second: the enforcement is at the door, not at the mouth.** Nobody hands a cleared officer the entire file and asks them to be careful about which parts they discuss. The material they don't need never enters the room. That's not because officers are untrustworthy — it's because a system that depends on every person's judgment on every occasion is a system with a known failure rate, and the failures are unrecoverable.

**That's the argument, and I'd make it as strongly as this:** compartmentalization is the only approach to sensitive information that has ever actually worked at scale, and it works precisely because it doesn't rely on the discretion of the person holding the information. Every other approach — rules, policies, training, review — is a filter applied *after* someone already has the material. Filters fail open. A compartment fails toward less.

**Now the translation, and it's almost one-to-one.**

Being an adult in the household is a clearance. It is not access. Being an enrolled caregiver is a clearance. It is not access either — it gets you into the compartments your actual care role requires, and no others. A daughter managing medications is read into medications. That does not read her into her father's finances, and no amount of her being helpful, present, or trusted changes it.

When a second caregiver joins, they don't inherit the history. They're read into what's current — the medications, the allergies, the care plan — because that's what the job requires today. The past requires a separate, deliberate, recorded grant. **History is not a fringe benefit of showing up.**

And the sharpest version, the one I'd lead with in a technical room: **the AI itself gets read in per question, and read out when the question ends.** It is not a cleared employee with standing access to the household. It is a contractor brought into one compartment for one meeting, handed exactly the material that meeting requires, and walked out. The next question is a new read-in. It never accumulates.

That's why we can say a model cannot decline to reveal what it never saw. It's not a clever prompt. It's the same structure that's protected sensitive material for eighty years, applied to a machine that's a far better candidate for it than a person is — because unlike a person, the compartment boundary can be enforced mechanically instead of by good faith.

> **Breaking point one, and it's the famous one:** compartmentalization has a catastrophic failure mode, and it has a date on it. Before September 2001, the compartments were exactly why nobody connected the dots. Everyone was doing their job correctly and the picture existed nowhere. In a house, that's the second caregiver who never sees "Dad fell this morning" and gives him another dose. **This is not a hypothetical for us — it's the reason our default is that care facts are visible to the whole enrolled care team rather than private to whoever wrote them.** Between a failure that's embarrassing and a failure that's medical, we take the embarrassing one. That's a deliberate loosening of the compartment, and I'd rather explain it than have someone discover it.
>
> **Breaking point two:** the intelligence world's own biggest failures were people with legitimate access to the compartments they leaked. Need-to-know doesn't solve the insider. It shrinks the blast radius and it makes the list of suspects short. Ours does the same and no more — if the person holding the key is the problem, this architecture has made them more powerful, not less.
>
> **Breaking point three, the honest one about reading out:** in the intelligence world, being read out is a signature on a form. It's a legal control, not a technical one — nobody can reach into your head. Ours is the same. We can stop future access immediately and rotate the keys so the old ones open nothing. We cannot make someone unremember what they already read. "Revoked" means no new access. It does not mean it never happened.

*Status: the per-question read-in — the AI receiving only the facts a specific question requires — is **built and proven**, and it's the demonstrable core of the product. Reading a new caregiver into current-but-not-historical material is **specified, not built**, and the requirement covering care-team access is one we've formally marked as not met. Reading out — revocation with key rotation — is **partially built**, with the "cannot unremember" limit stated as permanent.*

---

## PART TWO — THE FOUR GOVERNANCE PIECES

### PIECE ONE — THE BRIEFING PACKET
*(what we hold back before the AI is asked anything)*

If you need someone to give a briefing and there's an informant whose name can't get out, you don't hand them the full file and say "don't mention the informant." You hand them a folder that doesn't have the informant in it. No discipline required, no judgment call, no bad day.

That's what happens before every question. The AI gets a folder assembled for the person asking.

> **Breaking point:** a real briefer notices the gap. They can see the folder is thin and can ask about it. Same weakness here — a person can learn to read the silences. Withholding is much stronger than instructing. It is not invisible.

**Caveat I volunteer, because finding it cost us something:** we found places where the AI was refusing on its own — being careful, sounding responsible — rather than because we'd actually withheld anything. A polite refusal and a real one look identical from the outside. So we built a test that reads the execution record underneath instead of grading how the answer sounded.

*Status: **proven.***

### PIECE TWO — WHAT THE SYSTEM IS LICENSED TO CONCLUDE

A home health nurse handles enormous private information — medications, confusion, the bathroom, the finances on the kitchen table. And they still cannot declare you legally incompetent. Not because they haven't seen enough. Because that conclusion isn't theirs to draw.

That's the shape of our limits. Not how much the system knows — what it's allowed to conclude and write down.

**The line that lands:** consent does not expand scope. A patient cannot authorize their nurse to perform surgery. You can give our system permission to know things. You cannot give it permission to decide you have dementia.

Concretely: it may notice a medication reminder went unanswered three times. It may not write down that your mother is non-compliant. It may record the assistance she receives. It may not convert that into a theory about her mind.

> **Breaking point:** a nurse's license is enforced by an outside board. Ours is enforced by us, in our own code. That's weaker, and it's why the record and the outside copy of it matter more than the promise. The right question isn't "what are your rules," it's "who checks."

*Status: **proven**, with the limit stated in the ruling itself — two of its four parts hold because no code anywhere does the forbidden thing (sixteen files read to confirm it), and nobody is watching for someone writing that code later. The watcher is authorized and not built.*

### PIECE THREE — THE EVIDENCE ROOM

In a properly run evidence room, nothing goes on the shelf unlabeled. And there's no miscellaneous bin — because miscellaneous is how the wrong thing gets in and stays in. The absence of that bin is the design.

Every fact gets labeled at the door: what kind of thing it is, who it's about, how sensitive, who may see it, whether it may leave the house. If the label can't be determined, it doesn't get filed.

That last sentence used to be false. That's Story One.

> **Breaking point:** an evidence room protects objects that sit still. Our facts get combined. Two harmless things can join into something that isn't, and the new thing needs its own label. Harder than shelving, and it's why the nurse's-license piece exists alongside this one.

*Status: **proven**, both the labeling at the door and the kind-of-record labeling. Three limits ride along and get said out loud: two kinds of label still can't be assigned without reading what a person actually said, and we've banned ourselves from reading it for now; one has no assigning signal at all; and the never-store hole in Story One is still open.*

### PIECE FOUR — THE PHARMACIST

A good pharmacist won't sell you more just because you're willing to buy. Being an easy sell is not a medical indication.

Every consumer product works the opposite way. Say yes readily, get asked more. That's Story Two.

> **Breaking point:** a pharmacist has a career to lose. Software has nothing equivalent. The only thing that makes this real is whether the mechanism makes the trick impossible rather than discouraged. **Half of ours is now real code and half of it is nothing.**

*Status: **the enforcement half is built** — what counts as a real reason to ask, what explicitly does not count, and a gate allowing one offer per situation. **The behavior half does not exist:** nothing in the live system can make an offer at all, and none of the four kinds of real-world change can be represented yet. Rules without a mouth.*

---

## PART THREE — THE MOVING PARTS

*(Say this before the storage and routing sections. Without it, the room hears governance rules floating in space with no machine underneath them.)*

### FIRST, A NAMING PROBLEM I'LL SOLVE OUT LOUD

There's a layer in this system that finds patterns across everything a household has told it. It's built and it's running.

**I do not call it a learning layer, and neither should anyone repeating this.** Nothing in our system learns. No weights change. No model gets better because your household used it. That word would be a false claim and it's the kind that gets caught.

**Call it the pattern layer.** It reasons over what's accumulated. It does not train on it.

That distinction is worth more than it costs. Half this category is quietly saying "the more you use it, the more it learns about you," which is also a description of the thing people are afraid of.

### THE FOUR PLACES A MODEL TOUCHES THIS SYSTEM

**None of these is a model we trained.** We rent every one. What we built is what surrounds them.

**1. The listener.** A small model on the box in the house turns conversation into candidate facts. Somebody says "Dad's cardiologist moved his appointment to Thursday" and it proposes three facts. It proposes. It does not commit.

**2. The pattern layer.** Periodically looks across what's accumulated and proposes conclusions — connections the household never stated outright.

**3. The answering models.** One on the box, and outside services for harder questions. Covered in the routing section.

**4. The reordering model that does not exist.** More on that below, because its absence is a decision.

### THE TRACE — ONE SENTENCE THROUGH THE WHOLE MACHINE

This is the tie-back. Walk it slowly; it's the clearest sixty seconds in the pitch.

The daughter says: *"Dad's been forgetting his evening pills."*

1. **Voice takes it in** and hands over words. It holds no key to anything and cannot write to memory. It asserts who spoke; the system checks that independently.
2. **The listener proposes** a fact: subject Dad, kind medication-adherence, source the daughter.
3. **The labeler tags it at the door** — how sensitive, who may see it, whether it may ever leave the house. Unrecognized label means refused, not guessed. That's Story One.
4. **It's sealed** to the keys of the people entitled to it, and filed. The label on the outside stays readable so the system can find it later; the content doesn't.
5. **It enters as a claim, not a fact,** because it's about someone else. Dad or his custodian confirms it before it hardens.
6. **The record is written** — what came in, what was decided, why — and the head of that record is signed and copied somewhere the system cannot reach or alter.

Then, later, the other daughter asks: *"Is Dad doing okay with his medications?"*

7. **The read-in happens.** The system assembles a folder for *her specifically* — the facts her care role entitles her to, and no others.
8. **Routing decides** whether this is answerable on the box or needs an outside service, and what may cross that line.
9. **The model is handed the folder** and answers from it. If the folder is empty, it says so and stops rather than constructing something plausible.
10. **The whole decision is recorded**, and it's checkable afterward — including whether the refusal was structural or the model just being cautious.

**Nine of those ten steps happen whether or not a model behaves well.** That's the point of the whole architecture: the model is one component sitting in the middle of a machine that decided what it would see before it saw anything.

### THE PATTERN LAYER — AND THE PROPERTY THAT SURPRISES PEOPLE

The pattern layer looks at what's accumulated and proposes conclusions. "There's a medication adherence issue" is exactly the kind of thing it produces.

That's obviously the most dangerous component in the building, so here's what constrains it — all of it built, all of it enforced in code:

- **It needs at least two supporting facts, and it must name them.** No conclusion from a single data point.
- **Anything it produces is marked low-confidence and cannot promote itself.** Only a human confirming it can raise its standing. **The system cannot upgrade its own guesses.**
- **It stays inside one person's scope.** No conclusions that reach across people.
- **Take away a supporting fact and the conclusion dies with it.** Retracting a source kills what was concluded from it — that's tested.

**And the property that stops the room:** the pattern layer does not see what anyone said. It receives the *kinds* of facts and how well established they are — never the values. It can see that there's a medication fact, an incident, and an appointment about the same person in the same two weeks. **It cannot read what the medication is.** It reasons about the shape, not the content.

> **The analogy:** a night-shift clerk working from the index cards, not the files. She can see three folders were pulled on the same person in one week and flag it. She has never opened one.
>
> **Breaking point, and it's a real one:** the shape is often enough. Three medication facts, an incident, and a cardiology appointment in the same fortnight tells you a great deal without a single value. Metadata-only is a meaningful narrowing of what this component can reach. It is not the same as blind, and I won't claim it is.

**What governs the kind of conclusion it may draw — and the honest shape of that proof.** There's a written permission naming what may go into a conclusion and what may come out. It's built, it's enforced at the point of writing, it's tested, and we've accepted it as proven. Two of its four parts I'd describe carefully: the rule that the system can never widen its own authority to conclude, and the rule that it never concludes anything from a *missing* record, are true today because we read sixteen files and found no code that does either. **That's absence verified, not a guard standing watch.** Nobody is monitoring for someone writing that code next year. The check that would catch it is authorized and filed, and it is not built. I'd rather you hear "it holds because nothing does it" than let you assume something is patrolling.

The fourth part is different and it's actively tested: the system's scratch reasoning — the working-out on the way to a conclusion — is never saved anywhere. That one has nineteen live tests behind it.

**And one more, which is the sharpest live gap in the system.** Our governance controls what models *see* extremely well. The place it's thinnest is what models *cause* — the listener's output drives writes into memory, and that path doesn't have the same authority check the read path has. Model output is attacker-influenced input, and ours can write. It's filed, it's known, it's on the list, and it's the gap I'd attack first if I were on your side of the table.

*Status: the pattern layer's constraints and the retraction-kills-the-conclusion property are **proven**. The limits on what it may conclude are **proven, with two parts holding by verified absence and no watcher** — the watcher is authorized and filed as debt. The write-side authority gap is **known, filed, not closed**.*

### THE LEARNER THAT DOESN'T EXIST — AND THE FENCE WE BUILT ANYWAY

The obvious next question: shouldn't the system learn which facts matter to this household and get better at picking them?

Yes, and we're not doing it. **Which facts get retrieved is decided by rules, not by a learned system — and that's a position, not a queue item.** Rules can be audited. A learned ranker cannot. Auditability is the entire product claim, so we don't get to trade it for a few points of relevance. We revisit only if we measure a retrieval failure bad enough to justify the cost.

**Here's the part I'd actually put weight on.** Before building any learning component, we built the check that would catch a bad one — a validator that inspects every training example's origin and refuses anything that crosses between households or between people who shouldn't share a signal. It's wired at the strictest tier of our test suite. It passes. We proved it fails correctly by deliberately feeding it violations in both directions.

**It is currently guarding nothing, because there's no learner.** We built the fence before we got the animal. If anyone here later builds a learner that leaks, the fence goes red before it ships.

**And if we ever do build it,** the ruled design is: the shared piece trains only on public and synthetic data, and the piece that adapts to your household never leaves your house. The claim would be "your household's learning never leaves." **What I won't be able to claim** is the fashionable version — the math that lets many households train one model without exposing any of them needs thousands of participants per round to be meaningful, and at hundreds of households it isn't. If we ever pool, the honest word is "bounded influence," never "isolated." That's written down now, before there's any commercial pressure to blur it.

> **Breaking point:** a fence proves nothing about an animal that doesn't exist. The real test comes the day a learner arrives and someone finds it easier to move the fence than fix the learner. I can tell you the check is built and tested. I cannot tell you what the company does under that pressure — nobody can, and anyone who says otherwise is guessing about their own future.

*Status: rule-based retrieval is a **ruled position**, not a deferral. The isolation check is **built and proven**. The learner is **not built, and not scheduled**. The design for one, if it happens, is **specified with its limits already written down**.*

---

## PART FOUR — HOW IT'S ACTUALLY STORED

This is where a technical room starts paying attention, and where most companies get vague. Here's the whole thing.

### THE SEALED ENVELOPE, AND WHAT'S WRITTEN ON THE OUTSIDE

Every fact in the system is a sealed envelope. The contents are encrypted. But the outside of the envelope is readable — who said it, who it's about, what kind of fact it is, how sensitive it is, when it was said, how well established it is.

That's deliberate. If everything were sealed, the system couldn't find anything without opening every envelope in the building. Readable labels are what let it retrieve six relevant facts instead of decrypting ten thousand.

**And I'll say the cost out loud, because it's real:** someone who could read only the labels and never open anything would still learn that your father has twelve medication facts, four fall-related facts, and that his daughter contributed most of them. The shape of a life is visible even when the contents aren't. We chose that trade knowingly. Anyone who tells you their system encrypts everything and still searches instantly is describing something that doesn't exist yet.

> **Breaking point:** "encrypted" is the most oversold word in this industry. Ours means the contents of each fact are sealed, the labels aren't, and the search index is built only from the labels — never from what was said.

*Status: **proven** — including that the search index is built only from who-and-what-kind, never from the content.*

### THE SUPERINTENDENT'S MASTER KEY

Here's the part I'd want to hear from someone else, so I'll tell you first.

An apartment building's superintendent has a master key. It's convenient and it's the whole security problem — you're trusting a person, not a lock.

We started with one. A single key on the same machine as the database, able to open every fact in the house.

**What's done:** we rebuilt the locks. Facts are now sealed to individual people's keys instead. The old master key can no longer be used to derive a key for anyone — that path is closed in every place it used to exist, and we tested it by deliberately planting a violation to make sure the test would catch it. Everything currently in the store is on the new scheme.

**What isn't done:** the master key still exists on that machine. Until it's destroyed, the honest sentence is "the operator can't reach your facts through the old path" — not "the operator can't reach your facts."

**And the detail that shows you how this actually goes:** when we went to destroy it, we found the code silently creates a brand-new one the instant the file goes missing. It doesn't error. It doesn't refuse. So "destroyed" is not currently a state this system can be in. We found that by trying, not by reading the design. That's a small fix and it's the first item in the queue.

> **Breaking point:** even after destruction, this only covers data sitting still. It says nothing about the moment the system is actually answering a question. That's the next section, and it's the honest limit of the whole architecture.

*Status: the new locks are **proven**. Destruction of the master key is **built but not run** — with a known blocker we found ourselves.*

### THE SAFE DEPOSIT BOX — AND THE VIEWING ROOM

A bank can hold your box without seeing inside it. But when you want to look at what's in it, you carry it into one of the bank's rooms and open it there. For those few minutes, the contents are in the bank's building.

That's exactly our limit. Data at rest can be sealed so the operator can't read it. But to answer a question, the relevant facts have to be decrypted into working memory. Someone with full control of that machine, during that specific moment, could read that turn.

**The honest claim, stated in one breath:** the operator cannot read your data at rest — and at the moment of answering, the facts are in memory on their machine. Closing that requires specialized hardware that encrypts memory even from the machine's owner. We don't have it, we haven't built for it, and I'm not going to pretend it's coming next quarter.

**Why I'm comfortable saying that:** an outside security review of our testing reached the same conclusion independently, and named the same fix we'd already ruled out of scope. We're not conceding something we were hiding. We scoped it out on purpose and wrote down why.

> **Breaking point:** the box analogy makes it sound like a few seconds a month. It's every question. Someone with root on that box, watching continuously, sees every turn as it happens. The mitigation is that the box is in the operator's own facility under their own controls — which means this is a claim about who you're trusting, not a claim that nobody can see.

*Status: **out of scope by decision**, and stated as a limit rather than a roadmap item.*

### THE KEYLESS PERSON — THE HARDEST PROBLEM IN THE BUILDING

Here's the thing that makes household AI different from every enterprise system.

If facts are sealed to people's keys, what happens to the eighty-year-old who doesn't hold a key, doesn't want a phone, and is the person the system exists to help?

Our answer: the caregiver holds the key on his behalf. The unit of protection isn't the individual or the household — it's the pair. His facts become protected through the person caring for him.

**What that buys, and what it costs.** It means his private facts aren't readable by the whole house. It also means he is depending on the judgment of the person holding his key. Some of that is fixable — he can set standing rules that outrank any caregiver's decision, and those rules win. Some of it isn't. If a caregiver writes something down without marking it private, it's visible to the rest of the care team, and it can't be taken back.

**We chose that failure direction on purpose.** The other option — everything private by default — fails silently and it fails toward harm: the second caregiver doesn't see "Dad fell this morning" and gives him another dose. Care-team-visible by default fails toward embarrassment, and it fails with a warning, because the person writing it can see who'll be able to read it. Between a silent safety failure and a visible social one, we take the visible social one.

> **Breaking point:** none of this helps if the caregiver is the problem. A system that seals facts to a custodian's key has made that custodian more powerful, not less. We handle allegations by preserving them with attribution and routing to a human — the system never decides who's telling the truth. That's a real position and it is not a solution.

*Status: the two-person key structure is **built and proven**. Standing rules that outrank a caregiver are **designed, not built**.*

---

## PART FIVE — ROUTING: WHAT LEAVES THE HOUSE

### THE IN-HOUSE LAB AND THE OUTSIDE LAB

A hospital runs routine bloodwork in-house and sends the complex panels to an outside lab. Two questions govern everything: which work goes out, and what's on the sample when it does.

Same for us. Some questions get answered by a model running on the box in the house. Some go to an outside AI company, because that's where the capability is. Sensitivity decides which — and the most sensitive facts never leave, regardless of what's being asked.

**Then the second question, which is the one that matters:** what actually goes out. Not the whole file. A constructed packet.

**Where we're honest:** we have a mechanism that strips household facts out of what gets sent, and it does not cover every path. There are outbound paths where facts have reached the outside payload unfiltered. It's found, it's written down, it has an ID, and it's an open decision — extend the stripping to those paths, or accept and document it. It is not fixed today.

> **Breaking point:** removing the name doesn't remove the story. A stripped packet that still says "he's been hiding how much he drinks" is not anonymous to anyone who cares. Stripping identifiers is a real control and a weak one; the strong control is the sensitivity rule that keeps the fact from being eligible to leave at all.

*Status: the routing rule is **built**. The stripping mechanism is **built with a known gap**, open and documented.*

### THE ORDER WINDOW

There's a structural property here that's worth more than it sounds.

Households never talk to the AI service directly. They talk to our system, and our system builds the request. The household supplies a sentence. It does not supply the technical parameters of the request.

That sounds like plumbing. It's actually a defense. There's a published attack where a tenant on shared AI hardware can reconstruct a neighbor's prompt word by word — thousands of crafted requests, watching the response ordering for a signal. The attack requires the attacker to control the request parameters. In our shape, they can't: they're speaking to an assistant, not calling an API.

It's a fast-food order window rather than an open kitchen. You can order anything on the menu. You can't walk in and adjust the fryer.

> **Breaking point:** it's a boundary, not a wall. Anything that gets inside our system — a compromised process on the box, a scripted device — gets that control back. Which is why the same attack still deserves rate limits and traffic monitoring, and why I'd rather describe this as raising the cost than eliminating the attack.

*Status: the structural property is **real and inherent to the architecture**. The additional monitoring is **specified, not built** — and I'll note that the specification was cited in our own documents before it was actually written, which we caught and corrected.*

### AND THE PART I WON'T OVERSELL

When many households share one AI chip, the specialized memory-encrypting hardware everyone points to does *not* separate one household from another. It protects all of them from the machine's owner, together, in the same sealed room. Separating tenant from tenant cryptographically at the moment of answering means giving each one their own chip — which destroys the economics that make shared serving worth doing.

So our stated position: a shared model for most households, with separation enforced by request scoping. A dedicated chip for anyone who requires cryptographic separation, and they pay for the utilization they give up. Many households running their *own private models* on one shared chip — the thing that would be ideal — **we do not offer, because no hardware fence exists inside a single chip today.** That may change as models get smaller. We don't depend on it changing.

> **Breaking point:** "isolation by request scoping" is software isolation, not hardware isolation. It's the same boundary we already enforce between members of one household, applied one level up. I should not — and don't — describe it as a hardware guarantee.

---

## PART SIX — WHAT IT'S ACTUALLY LIKE TO USE

### THE RECEPTIONIST WITH NO KEYS

Voice is the product people imagine. It's also the least trustworthy component in any system like this — speech models are complex, they parse whatever sound arrives, and they change constantly.

Our position: voice is untrusted permanently, on purpose, no matter whose voice technology it is. We don't try to secure the voice stack. We make the boundary hold regardless of what's on the other side. Two hard rules: the voice component never holds a key to the facts, and it never runs in the part of the system that can write to memory.

Think of a receptionist who takes messages and hands them through a slot. No keys, no filing cabinet access.

**The problem that creates, which I'll name because it's the interesting one:** voice is also what recognizes who's speaking. So voice tells the system who you are, and everything downstream faithfully enforces whatever it was told. A compromised voice component doesn't have to break any of our rules — it just claims to be someone else. Our answer is that voice asserts and the system verifies independently, neither trusted alone. That's a design position with a real cost — it means voice has to hand over the audio, not just the words.

> **Breaking point, and it's a big one:** in the current deployment, the receptionist is sitting inside the vault. The voice components run in the same process that holds the database credential. That's the exact inversion of what we've ruled. It's the top item on the structural work, we know what it costs to fix, and it isn't fixed.

*Status: the boundary is **ruled and specified**. The deployment **does not match it yet**, and I'd rather tell you that than have you find it.*

### THE FIVE MODES, AND WHY WE'RE ONLY USING TWO

There's a natural progression for how you talk to something like this: typing; push-to-talk; the system speaking back; full duplex where you can interrupt it; and finally ambient, where it's just listening in the room.

**We're on the first two, deliberately.** Ambient listening is the one everybody demos and it's the one that requires the most trust from the household. We're not turning it on until the governance underneath it is proven. The restraint is the point — an always-listening device with unproven collection limits is precisely the product we're arguing against.

> **Breaking point:** this reads as principle and it's partly capability. Full duplex is genuinely hard and we haven't built it. Both are true and I'd rather state both than take credit for restraint I'm also being forced into.

*Status: modes one and two **live**. Modes four and five **deliberately stubbed**, with the reason written down.*

### THE FIRST CONVERSATION

Somebody has to tell the system who lives here. We've designed that as a guided conversation rather than a form — a narrator walks the household through it in four passes, starting with what people are happy to talk about and working toward the sensitive material. It's resumable; nobody has to finish in one sitting.

Two rules inside it matter. Anything you say about another person enters as a *claim*, not a fact, until that person confirms it. And a person responsible for someone who can't answer for themselves confirms every fact about them one at a time — including facts they supplied. The asking is the accountability.

> **Breaking point, and it's a genuine open problem:** asking someone to confirm forty things one at a time doesn't produce forty careful decisions. It produces habituation. The evidence on consent fatigue is against us here. We know that, it's an open item, and we have not solved it.

*Status: **designed, not built.** No requirement written, no code.*

### THE ANSWER YOU GET WHEN THERE'S NOTHING TO SAY

One behavior worth demonstrating because it's counterintuitive: when the system has nothing confirmed on a topic, it says so and stops. It does not construct a plausible answer from what's nearby.

That sounds small. It's the difference between an assistant and a liability. We have a test that plants a fabrication and confirms the reply comes back as a refusal to guess, with the record showing the refusal was structural.

*Status: **built and proven**, and it's the single best thing to show live.*

---

## PART SEVEN — WHAT WE BUILD, WHAT WE RENT, WHAT WE'VE DELIBERATELY LEFT OUT

Say this section slowly. It's the one that separates you from everyone else in the category.

### WHAT WE BUILD — and it's a short list on purpose

The memory: a fact store that knows who said what, about whom, when, how well established it is, and what happened to it since. The governance: who may see which fact, under what conditions. The context assembly: choosing which few facts go into any given question. The record: an audit trail of every decision, and the tests that prove it.

### WHAT WE RENT

The AI models, at every tier. Speech recognition and synthesis. Voice recognition. The embedding models. The databases. The specialized hardware if we ever use it.

**The thesis in one line:** models commoditize, governed memory compounds. We don't want to be in the model business. Every dollar we don't spend there goes into the thing that gets more valuable with time rather than obsolete with the next release.

### WHAT WE'VE DELIBERATELY NOT BUILT — and this is the load-bearing half

Protection at the moment of answering. Always-on voice. A system that learns from your household's data. Federated learning. The assistant deciding on its own to start conversations. Many private models on one shared chip.

**And one that moved, which I'll flag because it moved recently.** Erasure used to be on this list. It isn't anymore — the record was rebuilt and per-fact and per-person erasure is now built and proven against test fixtures, with a machine-checkable report saying what was and wasn't removed. **What is still true: nothing in the live system can invoke it from a real request, nothing real has ever been erased, and anything written before the rebuild stays unerasable forever.** So the honest sentence is that we built the machinery and have not connected it. I'm not saying we can delete your data. I'm saying the mechanism exists and is proven where we could prove it.

Each of those is written down with the reason. That's the list I'd want to see from anyone claiming what we claim — and a document that says what it didn't build is worth more than one that describes the target as if it were the present. The version of our own architecture document that did the second thing is the version we threw out.

**One of these is a real position rather than a deferral:** retrieval stays rule-based. Not "until we can afford a learned system" — indefinitely. A rule-based system can be audited. A learned ranker can't be. Auditability *is* the product claim, so we don't get to trade it for a few points of relevance. We revisit only if we measure a retrieval failure that justifies the cost.

> **Breaking point:** rule-based retrieval will be worse than a learned system at finding the right six facts. I'm accepting a quality ceiling in exchange for being able to explain every retrieval. If someone in the room thinks that's the wrong trade, that's a legitimate disagreement about the product, not a misunderstanding.

---

## PART EIGHT — THE TECHNOLOGY WE'RE BETTING ON, AND THE BET WE'RE NOT MAKING

**What we assume:** models keep getting cheaper for a given level of capability. The published estimates range from roughly two to ten times a year depending on who's measuring and how — I'd present it as a range, because anyone quoting one number is picking the one that suits them. Directionally it means the model line in our cost model falls on its own.

**What we don't assume:** that any specific hardware capability arrives. Not memory-encrypting chips getting cheaper. Not the ability to fence off one chip into private compartments. If those land, cases open up. Nothing in the plan requires them.

**Where new capability actually plugs in:** cameras, sensors, whatever comes next — those are new sources of facts, and facts are already governed. A new input class doesn't need a new architecture; it needs a label at the door. Same for the thing people call a world model: for us, that's a predictive layer over one household's own history. It's the same substrate with more structure over it, not a separate bet.

> **Breaking point:** "it's all the same substrate" is the kind of line that's true in architecture and expensive in practice. Adding a camera means a new label vocabulary, a new sensitivity mapping, and a new set of things the system must never conclude from what it saw. Cheap in principle, real work in fact.

---

## PART NINE — THE ANCHOR STORIES

### STORY ONE — THE BUG WE FOUND *(the credibility moment — slow down here)*

A daughter tells the system her father has been hiding how much he's drinking.

That fact gets a sensitivity label, and the label does real work — who sees it, and whether it may leave the house. The code checked the label against a list of known labels. If the label wasn't on the list, it filled in "medium" and carried on.

Medium is allowed to leave the house.

So the most private thing anyone in that family said that month gets packaged up and sent to an outside AI company. No error. No alert. **Three separate places did this, and every one failed toward permitting.**

> **The bouncer who lets you in whenever he can't read your ID.** Not lazy — he was told to keep the line moving, and nobody comes back to complain that they got in.
>
> **Breaking point:** a bouncer's mistake is visible in the room and over by morning. A data leak is invisible and permanent. And someone told that bouncer to keep the line moving. That someone was us.

**Why it survived, and this generalizes past our company:** a failure that *blocks* something gets a phone call in ten minutes. A failure that *permits* something gets discovered years later by a journalist. Every incentive in software finds the first kind fast and the second kind never. Ask any company that says it protects data what they found when they went looking for permissive failures. Most have never looked, because nothing was broken.

**The fix:** all three refuse instead of guessing, and we removed the ability to specify a fallback entirely. Every safety valve we've built with a default in it eventually turned into a silent downgrade. The option isn't available anymore — to us either.

**The ending you have to volunteer.** Then we went looking for the same disease elsewhere and found it. We have six kinds of records the system will never store. One of them no longer has a working check behind it — not because anyone decided it was acceptable, but because the check depends on recognizing who a fact is about, and it doesn't recognize "Dad" or "the household" as identities. So the check couldn't do its job and we pulled it rather than let it pretend. Nothing reaches that hole today; it arms the first time a genuine outsider enters the picture. It's written down, assigned, and held in place by a standing test.

**Why tell you this:** because you were about to ask "so nothing mislabels anymore?" You'd have had it out of me in one question. Anyone can say their system is careful. Almost nobody tells you what they found when they went looking.

### STORY TWO — THE ASKING PROBLEM *(front-load the split: the rules are built, the behavior isn't)*

An app asks for your location. You say no. It asks again. The fourth time you tap yes so it stops. They didn't convince you — they outlasted you.

Now eldercare. Yes to "remind Dad about his afternoon pills." Then "since you're already getting reminders, would it help to see when he leaves the house?" Then "you've found this useful — should we share his sleep patterns with your sister?"

Each step small. Each using your last yes as the argument for the next. Nobody ever asks the real question — *do you want a system that tracks your father's movements and reports on him to his relatives* — because on day one you'd have said no. On day ninety you're already there and nobody made a decision.

**The root cause is one number:** the percentage who say yes. The moment a company measures it and tries to raise it, every technique above follows automatically. Nobody has to be a villain. The metric does the work.

**What we've committed to, as mechanisms rather than promises:**
- Ask only when something in the world changed — a diagnosis, a prescription, an incident. Never because you seem agreeable, never because time passed, never because you said yes last time.
- One ask per situation. Not one a week until you cave.
- Wording comes from a fixed set of reviewed templates. The AI fills in the facts; it never writes the persuasion and never learns which phrasings worked. **A system that can't learn what works can't get better at wearing you down.**
- A decline is never a fact about you. It's recorded for oversight — I won't claim it vanishes, because someone has to be able to check we're not over-asking. But it cannot enter your father's file, cannot be shown to your sister, cannot color his care, and there is no note saying you're resistant to care coordination. That note is the actual harm.
- The yes-rate can never be a performance target. Watchable by oversight, never a goal.

> **The question you should ask, and the answer:** who decides when the situation changed? If the system decides, it can manufacture situations and ask forever. The answer: a situation changes when a fact about the world changes. Never elapsed time, never receptiveness. If that boundary is soft, the whole mechanism is theater — which is exactly what to check when we say it's built.

*Status: **split, and say it that way.** The list of what counts as a real reason to ask, the list of things that explicitly don't count — agreeableness, elapsed time, a previous yes — and the gate that permits one offer per situation are **built, in code.** But **nothing in the live system can make an offer**, and none of the four kinds of real-world change can even be represented yet. So the constraints are real and the product behavior is absent. Anyone who hears this as "they shipped ethical consent" has heard it wrong, and it's my job to stop that.*

---

## PART TEN — SO WHAT'S THE ACTUAL ADVANTAGE

Straight answer, then the argument against it.

**1. The unit of protection is the household, not the user.** Every assistant on the market is built for one person with one account. A house has people whose interests genuinely conflict — a daughter who needs to know, a father who'd rather she didn't, a second caregiver who shouldn't see what the first one wrote. Nobody is building for that, because the enterprise version of this problem is "different departments" and the consumer version is "one login." This is a third thing and it's where eldercare actually lives.

**2. The record is the product.** Every decision the system makes is written down as it happens, and copies go somewhere the system can't reach or alter. That means a skeptical engineer can be handed the thing and told to try to break it — and the answer to "did it really refuse for the reason you claim" is checkable rather than asserted. Most demos in this category cannot survive that.

**3. One mechanism I'd defend as genuinely novel:** when the system needs a person to confirm something, that confirmation cannot come through the AI. It's a separate channel — exact words, no interpretation, no model involvement whatsoever, and identity comes from who's authenticated in the conversation rather than from anything said out loud. Which means an attack that convinces the AI to do something cannot use the same AI to approve it. People are actively working on this problem right now and mostly not landing this shape.

**4. The compounding asset:** a household's governed history. Years of who said what, corrected by whom, superseded when. Nobody can buy that, and nobody can lawfully train on someone else's.

**Now the argument against all of it, which I'd rather make than have made at me.** Items 1 and 2 are engineering discipline, not invention — a well-funded team could copy them; they'd need eighteen months and the willingness to do unglamorous work, and most won't, but "most won't" isn't a moat. Item 3 is the only piece a patent attorney would look at twice, and a patent publishes in eighteen months, which teaches it to exactly the companies I'd least like to teach. Item 4 is real and it's the one nobody can shortcut — and it's also the one that requires us to be in a household long enough for it to accumulate, which is a distribution problem, not a technology problem.

**So the honest version:** the technology advantage is a head start and a set of positions competitors would have to reverse to catch up. The durable advantage is the accumulated context and whatever operator relationship gets us into the house. If someone tells you their AI privacy architecture is a moat, they're selling.

---

## PART ELEVEN — THE HONEST NUMBER

Thirty requirements. Eleven proven. **None failing.** Nineteen have never had their test run — and most of those nineteen can't run, because the thing they'd test isn't built.

I lead with that on purpose. It doesn't say we're a quarter done. It says we have a system that tells us what we haven't proven. Most teams can't produce that number — not because it's zero, because nobody's counting.

Every requirement has a written test defining what would count as proof. Until it runs, the requirement reads "not proven" — even when the code is written and obviously works. We've had cases where a test passed and we still didn't mark the requirement met, because passing one test isn't proving the requirement. That's happened five times and it's recorded each time.

> **Breaking point, and it cuts both ways.** Nineteen unrun tests is not nineteen broken things — most can't be tested because the thing they'd test isn't built. It's a count of missing proof, not a defect count. **And "none failing" does not mean nothing is wrong.** It means nothing on that board is currently sitting in the failed column. There are known defects and known debt underneath it, and I've named several of them already tonight. If I let you hear "none failing" as "nothing wrong," I've done exactly the thing this whole talk is against.

---

## PART TWELVE — THE RECAP

Read this out. Don't paraphrase.

**Dated 2026-08-05.** This board moves — six items moved in the two days before this version. If it's been more than a week, check it before you speak it.

### PROVEN — built, tested, formally accepted
- **Unrecognized sensitivity labels refuse instead of guessing**, in all three places that used to guess — and the fallback option is gone from the system entirely.
- **One sensitivity rulebook**, used everywhere, failing safely everywhere.
- **Facts are sealed to individual people's keys.** The old master path can no longer derive anyone's key; that's closed everywhere it existed, and we proved the test would catch a violation by planting one.
- **The search index is built only from who-and-what-kind, never from content.**
- **The two-person key structure** — a caregiver holding a key on behalf of someone who has none.
- **You can read back your own words; you cannot build a file on someone.**
- **Refusals are structural**, verified against the execution record rather than how the answer sounds.
- **The system says it doesn't know rather than constructing a plausible answer** — with a planted-fabrication test proving it.
- **An audit record copied where the system cannot reach or alter it.**
- **The limits on what the system may conclude** — with two of four parts holding by verified absence and no watcher, and the watcher filed as debt.
- **The kind-of-record labeling**, including a marker on any fact the system can't honestly label, naming which labels it might be instead of silently borrowing a neighbour's.
- **Erasure** — per-fact and per-person, proven against test fixtures with a machine-checkable completeness report.
- **A conclusion dies when a supporting fact is taken back**, and the pattern layer's constraints hold — two supporting facts minimum and named, no promoting its own confidence, scope-bound.
- **The check that would catch a leaky learning component** — built, tested in both directions, currently guarding nothing because no learner exists.

### BUILT, PROOF NOT ACCEPTED
- **The four checks at the door.** All four fire today. Two of them lean on rules that hold by verified absence rather than by a guard standing watch, which is why I keep this line here rather than in the proven list.
- **Destruction of the master key.** Preconditions done; the destruction step has not run, and we found the system silently regenerates the key if it goes missing.
- **The mechanism that strips household facts from outbound requests.** Real, and it does not cover every path. Open and documented.
- **The write side of model output.** Governance controls what models see; the path where model output causes a write does not have the same authority check. Filed, known, open.
- **Separation of our development and demo environments.**

### DESIGNED OR RULED, NOT BUILT
- **The asking mechanism's user-facing half.** The enforcement pieces are built — the list of what counts as a real reason to ask, the list of things that explicitly don't count, and the gate that allows one offer per situation. **Nothing in the live system can actually make an offer.** No offer mechanism exists, and none of the four kinds of real-world change can be represented yet. The rules exist; the behavior doesn't.
- **Erasure that anyone can actually invoke.** The erasure itself is built and proven — see above. But nothing in the live system reaches it from a real request, nothing real has ever been erased, and everything written before the rebuild stays unerasable permanently. **Do not say "we can delete your data."** Say the machinery exists, is proven against fixtures, and is not connected to anything a person can press.
- **Expiration.** Nothing ages out yet.
- **Limits on care-team access.** Partially built, known wrong in a documented way.
- **Standing rules a person sets that outrank any caregiver's decision.**
- **The first-conversation onboarding.** No requirement written, no code.
- **The voice boundary.** Ruled and specified; the current deployment runs voice in the same process that can write to memory, which is the inversion of the ruling.
- **Traffic monitoring for the shared-hardware attack.** Specified; and the specification was cited in our own documents before it was written, which we caught ourselves.

### OUT OF SCOPE BY DECISION — not a roadmap item
- **Protection at the moment of answering.** Facts are decrypted into memory to be used. Requires hardware we don't have and aren't planning around. An outside review reached the same conclusion independently.
- **Many private models sharing one chip.** No hardware fence exists inside a chip today.
- **A learned retrieval system.** Rule-based indefinitely, because auditability is the product claim. Nothing in the system learns; no weights change because a household used it.
- **Always-on ambient voice and full duplex**, until the governance underneath proves out.

### THE ONE-LINE VERSION
> The first list we've proven. The second is running but not proven. The third is written down and not built. The fourth we've decided not to do and I'll tell you why. You'll get told which one you're looking at every time you ask.

---

## APPENDIX — EVERY BREAKING POINT IN ONE PLACE

| Analogy | Breaking point to say first |
|---|---|
| Need to know / compartments | Compartments are why nobody connected the dots before 9/11. Ours loosens deliberately for care facts — say so first. |
| Being read in | Doesn't stop the insider with legitimate access. It shrinks the blast radius and shortens the suspect list. |
| Being read out | A signature on a form, not a technical control. We stop future access; we cannot make someone unremember. |
| Briefing packet | The briefer notices the folder is thin. Withholding beats instructing but isn't invisible. |
| Nurse's license | A nurse is policed by an outside board; we police ourselves. Ask who checks. |
| Evidence room | Evidence sits still. Facts combine, and the combination needs its own label. |
| Pharmacist | A pharmacist can lose a career. Software is only restrained by what it can't do — and ours isn't built. |
| The bouncer | His mistake is over by morning. A leak is permanent and invisible. And we told him to keep the line moving. |
| Night-shift clerk / index cards | The shape is often enough. Metadata-only narrows what the pattern layer reaches; it is not the same as blind. |
| Fence before the animal | A fence proves nothing about an animal that doesn't exist. The test comes when moving it is easier than fixing the learner. |
| Sealed envelope | The label is readable. The shape of a life shows even when the contents don't. |
| Superintendent's master key | Destruction only covers data at rest — and the system currently regenerates the key if you delete it. |
| Safe deposit box / viewing room | It's not a few minutes a month. It's every question. The mitigation is who owns the building, not that nobody can see. |
| Keyless person / custodian | Sealing to a custodian's key makes the custodian more powerful. If the caregiver is the threat, this doesn't help. |
| In-house lab / outside lab | Removing the name doesn't remove the story. Stripping is the weak control; not being eligible to leave is the strong one. |
| The order window | A boundary, not a wall. Anything that gets inside the system gets that control back. |
| Receptionist with no keys | In today's deployment the receptionist is sitting inside the vault. |
| Five modes, using two | Partly principle, partly capability. Say both. |
| First conversation | Forty confirmations doesn't produce forty decisions. The consent-fatigue evidence is against us. |
| Same substrate, new inputs | Cheap in architecture, real work in fact — every new input class needs its own labels and its own prohibitions. |
| Thirty requirements, eleven proven, none failing | Unrun is missing proof, not defects. And "none failing" is not "nothing wrong" — there are known defects and debt underneath the board. |
