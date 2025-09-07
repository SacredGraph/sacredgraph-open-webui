<script lang="ts">
	import { decode } from 'html-entities';
	import { createEventDispatcher } from 'svelte';
	import DomainAvailableModal from '../chat/DomainAvailableModal.svelte';
	import DomainUnavailableModal from '../chat/DomainUnavailableModal.svelte';
	import Spinner from '../common/Spinner.svelte';
	import Check from '../icons/Check.svelte';
	import XMark from '../icons/XMark.svelte';

	const dispatch = createEventDispatcher();
	$: dispatch('change', title);

	export let title: string;
	export let attributes: { arguments: string; result: string; done: string };
	export let className = 'my-2';
	export let buttonClassName =
		'w-fit text-gray-600 dark:text-gray-500 hover:text-gray-800 dark:hover:text-gray-300 transition border border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 rounded-lg px-2 py-0.5';

	export let id = '';

	let showModal = false;

	function parseJSONString(str: string): any {
		try {
			return parseJSONString(JSON.parse(str));
		} catch (e) {
			return str;
		}
	}

	function extractDomain(str: string): string {
		const { domain: rawDomain } = parseJSONString(decode(attributes?.arguments));
		return rawDomain.replaceAll('*', '');
	}
	function extractWhoisData(str: string): string {
		const { details } = parseJSONString(decode(str));
		return details;
	}

	function extractAvailability(str: string): boolean {
		const { available } = parseJSONString(decode(str));
		return available;
	}
</script>

<div {id} class={className}>
	<div
		class="{buttonClassName} cursor-pointer"
		on:pointerup={() => {
			showModal = true;
		}}
	>
		<div
			class=" w-full font-medium flex items-center justify-between gap-2 {attributes?.done &&
			attributes?.done !== 'true'
				? 'shimmer'
				: ''}
			"
		>
			{#if attributes?.done && attributes?.done !== 'true'}
				{@const domain = extractDomain(attributes?.arguments)}

				<Spinner className="size-4" />
				<span>Checking {domain} availability...</span>
			{:else}
				{@const domain = extractDomain(attributes?.arguments)}
				{@const available = extractAvailability(attributes?.result)}

				{#if available}
					<DomainAvailableModal bind:show={showModal} {domain} />
					<Check className="size-5 text-green-500" />
					<span>{domain} is available</span>
				{:else}
					{@const whoisData = extractWhoisData(attributes?.result)}

					<DomainUnavailableModal bind:show={showModal} {domain} {whoisData} />
					<XMark className="size-5 text-red-500" />
					<span>{domain} is not available</span>
				{/if}
			{/if}
		</div>
	</div>
</div>
