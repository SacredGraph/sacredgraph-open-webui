<script lang="ts">
	import { WEBUI_API_BASE_URL } from '$lib/constants';
	import { socket } from '$lib/stores';
	import NumberFlow from '@number-flow/svelte';
	import { onMount } from 'svelte';

	let maxLookups = 0;
	let currentLookups = 0;
	let isLoading = true;

	const LOOKUPS: Record<string, number> = {
		'7ma4w1WE': 20, // Free
		'496E6dQX': 200, // Starter
		y9qA8q9A: 1000, // Growth
		jW7Rnr9q: 3000, // Pro
		EWBrYOWr: 10000, // Scale
		DmwYKy94: 1000 // Add-on
	};

	const updateMaxLookups = async () => {
		const userData = await window.Outseta.getUser();
		const planId = userData?.Account?.CurrentSubscription?.Plan?.Uid;
		const baseLookups = LOOKUPS[planId] || 0;

		const addOnLookups =
			userData?.Account?.CurrentSubscription?.SubscriptionAddOns?.reduce(
				(total: number, addOn: any) => {
					const quantity = (LOOKUPS[addOn.AddOn.Uid] || 0) * addOn.Quantity;
					return total + quantity;
				},
				0
			) || 0;

		maxLookups = baseLookups + addOnLookups;
	};

	const fetchLookupCount = async () => {
		try {
			const response = await fetch(`${WEBUI_API_BASE_URL}/domain_lookups/count`, {
				credentials: 'include'
			});
			if (response.ok) {
				currentLookups = Number(await response.text());
			}
		} catch (error) {
			console.error('Failed to fetch domain lookups count:', error);
		}
	};

	onMount(async () => {
		try {
			await new Promise((resolve) => {
				function checkOutseta() {
					if (window.Outseta) {
						resolve(true);
					} else {
						setTimeout(checkOutseta, 100);
					}
				}

				checkOutseta();
			});

			updateMaxLookups();

			window.Outseta.on('subscription.update', () => {
				updateMaxLookups();
			});

			await fetchLookupCount();

			$socket?.on('chat-events', async (event) => {
				const type = event?.data?.type ?? null;
				const data = event?.data?.data ?? null;

				if (data?.done === true) {
					await fetchLookupCount();
				}
			});
		} catch (error) {
			console.error('Failed to fetch user data or domain lookups count:', error);
		} finally {
			isLoading = false;
		}

		return () => {
			$socket?.off('chat-events');
			window.Outseta.off('profile.update');
		};
	});
</script>

<div
	class="p-4 flex flex-col space-y-4 rounded-xl bg-white/90 dark:bg-yellow-400/10 dark:text-gray-100 border border-gray-50 dark:border-yellow-400/20"
>
	<div class="flex flex-col space-y-2">
		<div class="flex justify-between items-center">
			<span class="text-sm font-medium">Domain Lookups</span>
			{#if isLoading}
				<span class="text-sm text-gray-500">
					<div class="h-4 w-16 bg-gray-200 dark:bg-gray-700 rounded animate-pulse" />
				</span>
			{:else}
				<span class="text-sm text-gray-500">
					<NumberFlow value={currentLookups} /> / <NumberFlow value={maxLookups} />
				</span>
			{/if}
		</div>
		<div class="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
			<div
				class="h-full bg-yellow-400 dark:bg-yellow-500 transition-all duration-300 ease-in-out"
				style="width: {maxLookups > 0 ? (currentLookups / maxLookups) * 100 : 0}%"
			/>
		</div>
	</div>

	<button
		class="text-xs font-bold bg-yellow-400 text-gray-900 hover:bg-yellow-500 px-4 py-1.5 rounded-full transition-colors duration-200"
		on:click={() => {
			window.Outseta.profile.open();
			window.Outseta.profile.setTab('plan');
		}}
	>
		Get More
	</button>
</div>
