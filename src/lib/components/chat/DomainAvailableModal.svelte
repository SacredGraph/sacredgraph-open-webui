<script lang="ts">
	import type { i18n as i18nType } from 'i18next';
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';

	import Modal from '../common/Modal.svelte';

	export let domain;
	export let show = false;

	const i18n = getContext<Writable<i18nType>>('i18n');

	const registrars = [
		{
			name: 'Namecheap',
			logo: 'https://www.google.com/s2/favicons?domain=namecheap.com&sz=128',
			url: `https://www.namecheap.com/domains/registration/results/?domain=${domain}`,
			price: '$1.50'
		},
		{
			name: 'GoDaddy',
			logo: 'https://www.google.com/s2/favicons?domain=godaddy.com&sz=128',
			url: `https://www.godaddy.com/domains/searchresults.aspx?domainToCheck=${domain}`,
			price: '$2.99'
		},
		{
			name: 'Porkbun',
			logo: 'https://www.google.com/s2/favicons?domain=porkbun.com&sz=128',
			url: `https://porkbun.com/checkout/search?q=${domain}`,
			price: '$3.99'
		},
		{
			name: 'Dynadot',
			logo: 'https://www.google.com/s2/favicons?domain=dynadot.com&sz=128',
			url: `https://www.dynadot.com/domain/search?domain=${domain}`,
			price: '$2.99'
		},
		{
			name: 'Hover',
			logo: 'https://www.google.com/s2/favicons?domain=hover.com&sz=128',
			url: `https://www.hover.com/domains/results?q=${domain}`,
			price: '$12.99'
		}
	];
</script>

<Modal bind:show size="md">
	<div>
		<div class=" flex justify-between dark:text-gray-300 px-5 pt-4 pb-0.5">
			<div class=" text-lg font-medium self-center">{$i18n.t('Domain is available')}</div>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					viewBox="0 0 20 20"
					fill="currentColor"
					class="w-5 h-5"
				>
					<path
						d="M6.28 5.22a.75.75 0 00-1.06 1.06L8.94 10l-3.72 3.72a.75.75 0 101.06 1.06L10 11.06l3.72 3.72a.75.75 0 101.06-1.06L11.06 10l3.72-3.72a.75.75 0 00-1.06-1.06L10 8.94 6.28 5.22z"
					/>
				</svg>
			</button>
		</div>

		<div class="flex flex-col w-full px-5 pb-5 dark:text-gray-200">
			<div class="text-sm text-gray-500 mb-4">
				{$i18n.t('The domain')} <span class="font-semibold text-white">{domain}</span>
				{$i18n.t(
					'is available for registration. Click on a registrar to continue with the purchase:'
				)}
			</div>

			<div class="flex flex-col gap-3">
				{#each registrars as registrar}
					<a
						href={registrar.url}
						target="_blank"
						rel="noopener noreferrer"
						class="flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-800 w-full px-4 py-3 rounded-xl transition cursor-pointer"
					>
						<div class="flex items-center gap-3">
							<img src={registrar.logo} alt={registrar.name} class="h-6 w-6 object-contain" />
							<div class="flex flex-col">
								<span class="font-medium">{registrar.name}</span>
								<span class="text-xs text-gray-500"
									>{$i18n.t('Starting from')} {registrar.price}/{$i18n.t('year')}</span
								>
							</div>
						</div>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							viewBox="0 0 20 20"
							fill="currentColor"
							class="w-5 h-5 text-gray-400"
						>
							<path
								fill-rule="evenodd"
								d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z"
								clip-rule="evenodd"
							/>
						</svg>
					</a>
				{/each}
			</div>
		</div>
	</div>
</Modal>
