<template>
	<div class="page-quill scrollable">
		<div class="page-header">
			<h1>Code</h1>
			<el-breadcrumb separator="/">
				<el-breadcrumb-item :to="{ path: '/' }"><i class="mdi mdi-home-outline"></i></el-breadcrumb-item>
				<el-breadcrumb-item>Components</el-breadcrumb-item>
				<el-breadcrumb-item>Editors</el-breadcrumb-item>
				<el-breadcrumb-item>Code</el-breadcrumb-item>
			</el-breadcrumb>
		</div>
		<div class="card-base card-shadow--medium">
			<codemirror v-model="code" :options="cmOptions" />
		</div>
		
		<h4><a href="https://github.com/surmon-china/vue-codemirror" target="_blank"><i class="mdi mdi-link-variant"></i> reference</a></h4>
	</div>
</template>

<script>
// import language js
import 'codemirror/mode/javascript/javascript.js'

// import theme style
import 'codemirror/theme/base16-dark.css'

export default {
	name: 'CodePage',
	data() {
		return {
			code: 'const a = 10',
			cmOptions: {
				tabSize: 4,
				mode: 'text/javascript',
				theme: 'base16-dark',
				lineNumbers: true,
				line: true,
				// more CodeMirror options...
			}
		}
	}
}
</script>

<style lang="scss">
</style>

