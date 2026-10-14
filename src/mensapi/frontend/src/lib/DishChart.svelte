<script lang="ts">
  import * as d3 from 'd3';
  let { nutrients, allergens } = $props();

  type Slice = {
	label: string;
	value: number;
  };


  let entries: Slice[] = $derived([
	{ label: 'Protein', value: nutrients.protein },
	{ label: 'Fat', value: nutrients.fat },
	{ label: 'Saturated Fat', value: nutrients.saturated_fat },
	{ label: 'Carbohydrates', value: nutrients.fat },
   ]);
  const colors = [
	'#000000',
	'#0284c7',
	'#38bdf8',
	'#bae6fd'
	] 

  let arcs = $derived(d3.pie<Slice>().value((d) => d.value)(entries))
  
  const radius = 100;
  const margin = 80;
  const view = radius + margin

  const arcGenerator = d3
	.arc<d3.PieArcDatum<Slice>>()
	.innerRadius(radius * 0.5)
	.outerRadius(radius);

  const labelGenerator = d3
	.arc<d3.PieArcDatum<Slice>>()
    .innerRadius((1.3 * radius))
    .outerRadius((1.3 * radius));
</script>

<svg viewBox="{-view} {-view} {view * 2} {view * 2}" width={view * 2} height={view * 2}>
	{#each arcs as val, i}
		<path d={arcGenerator(val) ?? ''} fill={colors[i]}>
			<title>{val.data.label}: {val.data.value} g</title>
		</path>
		<text
		  x="0"
		  y="0"
		  text-anchor="middle"
		  font-size="0.8em"
		  transform="translate({labelGenerator.centroid(val).join(' ')})"
		  >{val.data.label}
		</text>
		<text x="0" y="0" text-anchor="middle" font-size="15" font-weight="700">
		{Math.round(nutrients.kcal)} kcal
		</text>
		<text
		  x="0"
		  y="1.2em"
		  text-anchor="middle"
		  font-size="0.8em"
		  font-weight="700"
		  transform="translate({labelGenerator.centroid(val).join(' ')})"
		  >{val.data.value + ' g'}
		</text>
	{/each}
</svg>
