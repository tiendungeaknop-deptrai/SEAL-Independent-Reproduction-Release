# Documented deviations

- Stable Diffusion 2.1 Base was obtained from `sd2-community/stable-diffusion-2-1-base` at revision `4e63672c03103b6c636b8fb4119ba982469b2955` because the source-referenced repository was unavailable. Relevant FP16 weight hashes matched an independent mirror in the private audit.
- Local memory placement moved BLIP-2 and sentence embedding inference to CPU where necessary; watermark-generation and detector parameters were unchanged.
- CAT used a fixed transparent-cat surrogate because the exact publication asset was unavailable. Publication sample size and some spatial-test semantics remain unresolved.
- Caption/embedding evaluates the released fine-tuned artifact, not its training process.
- Semantic-angle execution followed released-source scale with a documented implementation deviation; publication mapping remains unresolved.
- Generation-quality evidence covers Stable-Diffusion-Prompts only. The COCO metadata asset, split, annotation version, and ordering were not recoverable.

