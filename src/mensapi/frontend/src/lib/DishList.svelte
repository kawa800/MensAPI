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
			<div class="chart">
				<DishChart nutrients={dish.nutrients} allergens={dish.allergens}/>
			</div>
			{#if dish.allergens.length}
			<div class="table">
			<table class="allergens">
			  <thead>
				<tr>
				  <th scope="col">Allergens</th>
				</tr>
			  </thead>
			  <tbody>
				{#each dish.allergens as allergen}
				<tr>
					<td>{allergen.name}</td>
				</tr>
				{/each}
			  </tbody>
			</table>
			</div>
			 {:else}
			 {/if}
		</div>
	</div>
	{/each}
</div>


<style>
	.dish-grid {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 1rem;
	}

	.dish-component {
        display: flex;
        flex-direction: column;
        justify-content: space-between; /* Distributes internal spacing evenly */
    }
	
	.chart-with-list {
		display: grid;
		grid-template-columns: 10fr 1fr;
		align-items: flex-start;
		gap: 1em;
	}

	.price {
		font-size: 0.8em;
		color: #006BB2;
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
      border: 1px solid rgb(160 160 160);
      padding: 4px 6px; /* Reduced padding */
    }

	tr:nth-of-type(even) {
	  background-color: #eeeeee;
	}

	table {
      border-collapse: collapse;
      border: 2px solid rgb(140 140 140);
      font-family: sans-serif;
      font-size: 0.7rem; /* Reduced font size */
      letter-spacing: 0.5px;
    }

	caption {
	  caption-side: bottom;
	  padding: 10px;
     }
</style>
