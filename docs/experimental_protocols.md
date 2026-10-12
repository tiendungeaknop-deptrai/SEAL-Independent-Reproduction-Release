# Experimental protocols

## Clean detector

The detector used 1,024 latent patches, 7 SimHash bits, base seed 42, and 50 diffusion/inversion steps. Calibration (10 watermarked and 10 control images) selected threshold 1.5 and minimum match count 1. These values were frozen for disjoint held-out (20/20) and confirmatory (30/30) stages. The pooled 50/50 summary is secondary, not a third independent experiment.

## Transformation robustness

Thirty watermarked images and 30 random controls were evaluated under Clean, Rot75, JPEG25, CropScale75, Blur8, Noise0.1, and Brightness6. The exhaustive detector enumerated all 128 patterns for 7 bits and used source threshold 2.3. Missing publication metric/averaging detail and absence of an authorized comparison tolerance make the outcome inconclusive.

## CAT attack

Thirty paired clean/attacked source images were evaluated. The basic detector and two prespecified spatial interpretations were retained: SOURCE_LITERAL follows the released recovery helper, while PAPER_CONSISTENT uses deterministic SHA-256 hashing from the main generation path. Localization compares inside- and outside-box summaries within each attacked image. A fixed surrogate cat asset was necessary.

## Caption and embedding

Three configurations used 1,000 records each: direct CLIP image features, BLIP-2 captions with original MPNet, and BLIP-2 captions with the released fine-tuned MPNet artifact. The claim is the qualitative ordering of unrelated-minus-related angular gaps, not reproduction of the approximately 10k-pair embedding training process.

## Generation quality

One hundred paired Stable-Diffusion-Prompts test observations (indices 0–99) were evaluated at 512×512. The source-defined value is `CLIPModel(...).logits_per_image.item()`, not an external standardized CLIPScore. The paired delta interval used 10,000 bootstrap replicates at the paired-observation unit.

## Semantic angle

The released-source-scale run selected 549 records across 30 configured bins; 27 bins were populated. Publication mapping and the comparison rule remain unresolved, so the curve is descriptive and inconclusive.

