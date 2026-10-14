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
					Students: {dish.prices.price_students}€
				</p>
				<p>
					Non-Students: {dish.prices.price_non_students}€
				</p>
				
		</div>
		<DishChart nutrients={dish.nutrients} allergens={dish.allergens}/>
	</div>
{/each}
</div>

<style>
	.dish-grid{
		display: grid;
		justify-content: center;
		grid-template-columns: repeat(3, 1fr);
		gap: 1rem;
	}
</style>
