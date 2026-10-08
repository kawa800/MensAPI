<script lang="ts">
	import DishList from '$lib/DishList.svelte'
	let { data } = $props();
	
	const weekdays = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag'];
	let selectedDay = $state(weekdays[0]);
	$inspect(selectedDay);

	let dishesForDay= $derived(
		data.dishes.filter( (d) => d.day == selectedDay)
	);
	$inspect(dishesForDay)
</script>


<div class="tab">
	{#each weekdays as day}
		<button
			class:active={day == selectedDay}
			onclick={() => {
				selectedDay = day;
			}}
		>
			{day}
		</button>
	{/each}
</div>

<DishList dishes={dishesForDay} />


<style>
	.tab {
		display: flex;
		justify-content: center;
		gap: 0.5rem;
		margin-bottom: 1.5rem;
	}

	button {
		padding: 0.5rem 1rem;
		border: 1px solid #d6ebfb;
		background: #eaf4ff;
		border-radius: 6px;
		cursor: pointer;
	} 
	
	button.active {
		background: #006BB2;
		color: white;
	}
</style>
