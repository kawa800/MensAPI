<script lang="ts">
	import DishChart from '$lib/DishChart.svelte';
	let { dishes } = $props();
</script>


<div class="dish-grid">
{#each dishes as dish}
	<div class="dish-component"> 
		<div class="dish-header">
			<h3>{dish.name}</h3>
			<span class="price"> 
				<p>
					Students: {dish.prices.price_students} €
				</p>
				<p>
					Non-Students: {dish.prices.price_non_students} €
				</p>
		</div>
		<div class="chart-with-list">
			<DishChart nutrients={dish.nutrients} allergens={dish.allergens}/>

			<table class="allergens">
			  <thead>
				<tr>
				  <th scope="col">Allergens</th>
				</tr>
			  </thead>
			{#if dish.allergens.length}
			  <tbody>
				{#each dish.allergens as allergen}
				<tr>
					<td>{allergen.name}</td>
				</tr>
				{/each}
			  </tbody>
			 {:else}
				<tbody>
				<tr>
					<td> None </td>
				</tr>
				</tbody>
			  {/if}
			</table>
		</div>
	</div>
	{/each}
</div>


<style>
	.dish-grid {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 1rem;
	}

	.chart-with-list {
		display: flex;
		flex-wrap: nowrap;
		align-items: flex-start;
		gap: 1rem;
	}

	.price {
		font-size: 0.8em;
		color: #006BB2;
	} 


	.allergens {
		list-style: none;
		margin: 0;
		padding: 0;
		font-size: 0.85rem;
	}

	th,
	td {
	  border: 1px solid rgb(160 160 160);
	  padding: 8px 10px;
	}

	th[scope="col"] {
	  background-color: #505050;
	  color: white;
	}

	th[scope="row"] {
	  background-color: #d6ecd4;
	}

	td {
	  text-align: center;
	}

	tr:nth-of-type(even) {
	  background-color: #eeeeee;
	}

	table {
	  border-collapse: collapse;
	  border: 2px solid rgb(140 140 140);
	  font-family: sans-serif;
	  font-size: 0.8rem;
	  letter-spacing: 1px;
	}

	caption {
	  caption-side: bottom;
	  padding: 10px;
	  svg { width: 100%; max-width: 260px; height: auto; }}

</style>
