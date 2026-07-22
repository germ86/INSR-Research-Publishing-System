# Additional neuroclinical palette pack

INSR ships eight additional neutral scientific palettes for neuroclinical and translational documents:

| Palette | Intended use |
| --- | --- |
| `cortex-blue` | restrained neuroscience blue for papers and reports |
| `autonomic-teal` | teal clinical/autonomic-system visual language |
| `somatic-sage` | low-arousal sage palette for somatic and safety-focused material |
| `translational-plum` | translational research emphasis with muted plum accents |
| `nordic-neuro` | cool Nordic-style scientific palette |
| `clinical-burgundy` | formal clinical documents and protocols |
| `synapse-amber` | warm emphasis palette for methods and education |
| `nocturne-neural` | dark presentation palette; pair with `design/mode = dark` |

Select any palette with the existing public key:

```tex
\INSRConfigure{
  design/palette = cortex-blue
}
```

For `nocturne-neural`, also set `design/mode = dark` so semantic text, heading, header, footer and table-of-contents roles use the dark-mode contrast aliases.
