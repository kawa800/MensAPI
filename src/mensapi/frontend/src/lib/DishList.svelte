<script lang="ts">
	import DishChart from '$lib/DishChart.svelte';
	let { dishes } = $props();
</script>

{#each dishes as dish}
	<div class="dish-component"> 
		<div class="dish-header">
			<h3>{dish.name}</h3>
			<span class="price"> 
				<p>
					Students: {dish.prices.price_students}€
				</p>
				<p>
					Non-Students: {dish.prices.price_non_students}€
				</p>
				
		</div>
		<DishChart nutrients={dish.nutrients} allergens={dish.allergens}/>
	</div>
{/each}
