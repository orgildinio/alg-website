import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    category: z.enum(['Rebates & Codes', 'Spec Notes', 'Product News']),
    date: z.date(),
    author: z.string(),
    hero: z.string(),
    heroAlt: z.string(),
    excerpt: z.string(),
    supportingImage: z.string(),
    supportingImageAlt: z.string(),
    faq: z.array(z.object({ question: z.string(), answer: z.string() })),
    ctaLabel: z.string(),
    ctaHref: z.string(),
    featured: z.boolean().default(false),
  }),
});

export const collections = { blog };
