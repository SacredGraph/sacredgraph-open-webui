<script lang="ts">
	import type { i18n as i18nType } from 'i18next';
	import { getContext } from 'svelte';
	import type { Writable } from 'svelte/store';

	import Modal from '../common/Modal.svelte';

	export let domain;
	export let show = false;
	export let whoisData: string;

	const i18n = getContext<Writable<i18nType>>('i18n');

	function parseJSONString(str: string): any {
		try {
			return JSON.parse(str);
		} catch (e) {
			return str;
		}
	}

	function formatDate(dateStr: string): string {
		try {
			const date = new Date(dateStr);
			return date.toLocaleDateString(undefined, {
				year: 'numeric',
				month: 'long',
				day: 'numeric'
			});
		} catch (e) {
			return dateStr;
		}
	}

	function cleanString(str: string): string {
		return str.replace(/\*\*/g, '');
	}

	function getFormattedWhois(): { label: string; value: string }[] {
		try {
			const data = parseJSONString(whoisData);
			return [
				{
					label: 'Registrar',
					value: cleanString(data.registrar)
				},
				{
					label: 'Creation Date',
					value: formatDate(data.creation_date[0])
				},
				{
					label: 'Expiration Date',
					value: formatDate(data.expiration_date[0])
				}
			];
		} catch (e) {
			return [];
		}
	}
</script>

<Modal bind:show size="sm">
	<div>
		<div class="flex justify-between dark:text-gray-300 px-5 pt-4 pb-2">
			<div class="text-lg font-medium self-center">{$i18n.t('Domain is not available')}</div>
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
			<div class="text-sm text-gray-500">
				{$i18n.t('The domain')} <span class="text-black dark:text-white">{domain}</span>
				{$i18n.t('is not available for registration.')}
			</div>

			<div class="text-sm text-gray-500 mb-4">
				{$i18n.t('Here is the information about the domain:')}
			</div>

			<div class="space-y-4">
				{#each getFormattedWhois() as item}
					<div>
						<div class="text-sm text-gray-500 dark:text-gray-400 mb-1">
							{item.label}
						</div>
						<div class="text-sm text-gray-700 dark:text-gray-300">{item.value}</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</Modal>
