<script lang="ts">
	import favicon from '#lib/assets/favicon.svg';
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();
</script>

<nav>
	<a href="/">home</a>
</nav>



<enhanced:img class="logo-top-right" src= '../lib/assets/hhu-logo.webp' alt="The logo of Heinrich Heine university" />

<style>
:global(body) {
  background: #A2BFFE;   /* vivid cobalt, “more blue” */
  color: #0a2463;                /* dark blue text */
}

:global(main) {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
  min-height: 100vh;
}

.logo-top-right {
    position: absolute;
    top:      4px;
    right:    24px;   /* 24px from right edge */
    width:    128px;   /* exact pixel size */
    height:   auto;     /* keeps aspect; change manually if square */
    opacity:  0.9;     /* subtle blending */
  }
</style>


{@render children()}
