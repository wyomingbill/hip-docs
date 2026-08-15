# REQ_VOICE_DEMO
Status: PLAN
Reconciled-Against: b9770fb (2026-07-15)

## THE REQUIREMENT

Bill's words, verbatim:

> "There are two parts to this demo. There is the scripted part and there is
> the audio part. It's all in one. Once you get done with the scripted part,
> then you go to the audio part and start talking to it. And all the
> dashboard shit should work like it worked in the scripted."

Expanded: he talks a scripted line into the mic, then his transcript (VTT)
appears on screen, then a text response appears, then a spoken reply plays.
One screen, no terminal.

## THE ACCEPTANCE TEST

1. Open /demo.
2. Run a script to completion.
3. Click a control on that same screen, then speak.
4. His words appear on screen as he speaks.
5. A text reply appears.
6. Audio plays.
7. A record with tier=realtime lands in logs/turns_demo.jsonl.
8. A cross-member probe still refuses.
9. No terminal is touched at any point.

All nine or it is not done.

## WHAT'S ALREADY DONE

Do not redo any of these:

- GA session.update schema is FIXED: transcription and turn_detection nest
  under audio.input; voice under audio.output; output_modalities, not
  modalities; session.type='realtime'. Confirmed on the Mini:
  "session configured: modalities=['audio'] audio_keys=['input','output']",
  no error.
- Voice turns already emit d1.1 records (tier=realtime).
- LIVE mode already renders them.
- Governance already fires on voice.

## WHAT'S KNOWN BROKEN

- There is NO mic control on /demo. The LIVE button only switches which feed
  the panes poll. It starts nothing.
- The mic lives in scripts/realtime_voice_demo.py, a separate terminal
  process the dashboard cannot launch.
- That script also gates on "press ENTER to stop" while configuring
  turn_detection=server_vad. These are mutually exclusive designs, which
  produced "recorded 4295.8 s".

## CONSTRAINTS

- Do not break SCRIPT mode.
- Do not fork the panes: one set of renderers, both phases.
