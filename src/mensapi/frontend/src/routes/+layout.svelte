<script lang="ts">
	import favicon from '#lib/assets/favicon.svg';
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();
</script>

<header>
	<div class="top-bar">MensAPI — Mensa Menü der Heinrich-Heine-Universität Düsseldorf</div>
	<div class="header-bar">
		<nav>
			<a href="/api/docs">Dokumentation</a>
			<a href="/">Über uns</a>
		</nav>
		<enhanced:img class="logo" src="../lib/assets/hhu-logo.webp" alt="The logo of Heinrich Heine University" />
	</div>
</header>

<main>
	{@render children()}
</main>

<style>
	:global(body) {
		margin: 0;
		background: #ffffff;
		color: #1a1a1a;
		font-family: system-ui, -apple-system, 'Segoe UI', sans-serif;
	}

	.top-bar {
		background: #eaf4ff;
		color: #0369a1;
		font-size: 0.85rem;
		text-align: center;
		padding: 0.4rem 1rem;
		border-bottom: 1px solid #d6ebfb;
	}

	.header-bar {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem 2rem;
		border-bottom: 1px solid #eef2f6;
	}

	nav {
		display: flex;
		gap: 1.5rem;
	}

	nav a {
		color: #334155;
		text-decoration: none;
		font-weight: 500;
		font-size: 0.95rem;
		transition: color 0.15s ease;
	}

	nav a:hover {
		color: #0284c7;
	}

	.logo {
		width: 96px;
		height: auto;
	}

	:global(main) {
		max-width: 900px;
		margin: 0 auto;
		padding: 2rem 1.5rem;
	}
</style>
